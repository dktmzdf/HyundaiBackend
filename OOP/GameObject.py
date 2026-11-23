# ===== 공통 =====
class GameObject:
    def __init__(self, name):
        self.name = name


class HP:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.current = max_hp

    def damage(self, amount):
        self.current = max(0, self.current - amount)

    def heal_full(self):
        self.current = self.max_hp

    def is_alive(self):
        return self.current > 0


# ===== 재미 요소 ① 속성 상성 =====
class Element:
    STRONG = {"불": "풀", "풀": "물", "물": "불"}  # key가 value에 강함

    def __init__(self, name):
        self.name = name

    def multiplier(self, target):
        if Element.STRONG[self.name] == target.name:
            return 2.0
        if Element.STRONG[target.name] == self.name:
            return 0.5
        return 1.0


class Item:
    def __init__(self, name):
        self.name = name


class Weapon(Item):  # IS-A : 무기는 아이템이다
    def __init__(self, name, power, element):
        super().__init__(name)
        self.power = power
        self.element = element  # HAS-A : 무기는 속성을 갖는다
        self.enhance = 0

    def upgrade(self):
        self.enhance += 1
        self.power += 5

    def __str__(self):
        tag = f"+{self.enhance} " if self.enhance else ""
        return f"{tag}{self.name}[{self.element.name}]"


# ===== 재미 요소 ② 레벨 업 =====
class Level:
    def __init__(self):
        self.level = 1
        self.exp = 0

    def need(self):
        return self.level * 100

    def gain(self, amount):
        self.exp += amount
        up = 0
        while self.exp >= self.need():
            self.exp -= self.need()
            self.level += 1
            up += 1
        return up


# ===== 재미 요소 ③ 인벤토리 =====
class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add(self, item):
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def take(self, name):
        for item in self.items:
            if item.name == name:
                self.items.remove(item)
                return item
        return None


# ===== 몬스터 =====
class Monster(GameObject):
    def __init__(self, name, max_hp, element, exp_reward, drop=None):
        super().__init__(name)
        self.hp = HP(max_hp)
        self.element = element
        self.exp_reward = exp_reward
        self.drop = drop


class Slime(Monster):
    def __init__(self):
        super().__init__(
            "슬라임", 40, Element("풀"), 60, Weapon("물의 창", 25, Element("물"))
        )


class Golem(Monster):
    def __init__(self):
        super().__init__("골렘", 120, Element("풀"), 90, Item("강화석"))


class Dragon(Monster):
    def __init__(self):
        super().__init__("레드 드래곤", 300, Element("불"), 500)


# ===== 캐릭터 =====
class Character(GameObject):
    def __init__(self, name, max_hp, weapon):
        super().__init__(name)
        self.hp = HP(max_hp)  # HAS-A
        self.weapon = weapon  # HAS-A
        self.level = Level()  # HAS-A
        self.inventory = Inventory(5)  # HAS-A

    def attack(self, target):
        mult = self.weapon.element.multiplier(target.element)
        dmg = int(self.weapon.power * mult)
        target.hp.damage(dmg)
        log = [
            f"{self.name}의 {self.weapon} 공격! {target.name}에게 {dmg} 피해 (x{mult})"
        ]

        if not target.hp.is_alive():
            log.append(f"{target.name} 처치! EXP +{target.exp_reward}")
            up = self.level.gain(target.exp_reward)
            if up:
                self.hp.max_hp += 20 * up
                self.hp.heal_full()
                log.append(f"레벨 업! Lv.{self.level.level} (최대 HP {self.hp.max_hp})")
            if target.drop and self.inventory.add(target.drop):
                log.append(f"'{target.drop.name}' 획득!")
        return log

    def equip(self, name):
        item = self.inventory.take(name)
        if item is None or not isinstance(item, Weapon):
            return False
        self.inventory.add(self.weapon)
        self.weapon = item
        return True

    def upgrade_weapon(self):
        stone = self.inventory.take("강화석")
        if stone is None:
            return False
        self.weapon.upgrade()
        return True


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, 150, Weapon("화염검", 30, Element("불")))
