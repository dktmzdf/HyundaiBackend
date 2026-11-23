class Weapon:
    def __init__(self, name: str, power: int):
        self.name = name
        self.power = power

    def __repr__(self):
        return f"{self.name}(+{self.power})"


class Character:
    def __init__(self, name: str, hp: int, base_atk: int, weapon: Weapon | None = None):
        self.name = name
        self.hp = hp
        self.base_atk = base_atk
        self.weapon = weapon  # HAS-A: Character has-a Weapon

    @property
    def atk(self) -> int:
        return self.base_atk + (self.weapon.power if self.weapon else 0)

    def equip(self, weapon: Weapon):  # 구성의 장점: 런타임에 부품 교체
        print(f"{self.name}: {self.weapon} → {weapon} 장착")
        self.weapon = weapon

    def attack(self, target: "Character"):
        dealt = target.take_damage(self.atk)
        print(
            f"{self.name}의 공격! {target.name}에게 {dealt} 피해 (남은 HP {target.hp})"
        )

    def take_damage(self, dmg: int) -> int:  # 실제로 들어간 피해량 반환
        before = self.hp
        self.hp = max(0, self.hp - dmg)
        return before - self.hp

    @property
    def alive(self) -> bool:
        return self.hp > 0

class Warrior(Character):
    def __init__(self, name: str, weapon: Weapon | None = None):
        super().__init__(name, hp=120, base_atk=10, weapon=weapon)
        self.armor = 5

    def take_damage(self, dmg: int) -> int:  # 오버라이드: 방어력만큼 감소
        return super().take_damage(max(1, dmg - self.armor))


class Mage(Character):
    def __init__(self, name: str, weapon: Weapon | None = None):
        super().__init__(name, hp=70, base_atk=6, weapon=weapon)
        self.mp = 30

    def attack(self, target: Character):  # 오버라이드: MP가 있으면 마법(2배)
        if self.mp >= 10:
            self.mp -= 10
            dealt = target.take_damage(self.atk * 2)
            print(
                f"{self.name}의 파이어볼! {target.name}에게 {dealt} 피해 (MP {self.mp}, 남은 HP {target.hp})"
            )
        else:
            super().attack(target)


# ── 상속(IS-A): Dragon is-a Monster ("몬스터는 드래곤이다"는 어색 → 방향 확인)
class Monster(Character):
    def __init__(self, name: str, hp: int, base_atk: int, exp: int):
        super().__init__(name, hp, base_atk)
        self.exp = exp


class Dragon(Monster):
    def __init__(self):
        super().__init__("드래곤", hp=200, base_atk=18, exp=500)

    def attack(self, target: Character):
        print("🔥 드래곤이 브레스를 뿜는다!")
        super().attack(target)


# ── 실행 ──────────────────────────────────────────────────
if __name__ == "__main__":
    sword = Weapon("롱소드", 15)
    staff = Weapon("지팡이", 8)
    axe = Weapon("배틀액스", 25)

    w = Warrior("전사", sword)
    m = Mage("마법사", staff)
    d = Dragon()

    # 관계 확인
    print("Warrior is-a Character:", isinstance(w, Character))  # True
    print("Dragon is-a Monster:", isinstance(d, Monster))  # True
    print("Monster is-a Dragon:", issubclass(Monster, Dragon))  # False
    print("전사 has-a:", w.weapon)
    print()

    w.attack(d)
    m.attack(d)
    d.attack(w)
    w.equip(axe)  # 상속이었다면 클래스를 새로 만들어야 했을 변경
    w.attack(d)
    print(f"\n드래곤 생존 여부: {d.alive}")

    # 다형성: 같은 attack() 호출, 타입별로 다른 동작
    print("\n[파티 일제 공격]")
    for hero in (w, m):
        hero.attack(d)
