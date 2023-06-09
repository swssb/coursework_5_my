from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 3
    player = None
    enemy = None
    game_is_running = False
    battle_result = ""

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        """НАЧАЛО ИГРЫ"""
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> str:
        """ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И КОМПЬЮТЕРА И ЗАПИСЬ РЕЗУЛЬТАТА"""
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = 'Ничья'
            return self._end_game()
        if self.player.hp <= 0:
            self.battle_result = 'Игрок проиграл'
            return self._end_game()
        if self.enemy.hp <= 0:
            self.battle_result = 'Игрок выиграл'
            return self._end_game()

    def _stamina_regeneration(self) -> None:
        """ РЕГЕНЕРАЦИЯ ВЫНОСЛИВОСТИ КАЖДЫЙ РАУНД НА КОНСТАНТУ """
        if self.player.stamina + self.STAMINA_PER_ROUND * self.player.unit_class.stamina\
                <= int(self.player.unit_class.max_stamina):
            # print(self.player.stamina)
            # print(self.player.unit_class.stamina)
            # print(self.STAMINA_PER_ROUND)
            self.player.stamina += self.STAMINA_PER_ROUND * self.player.unit_class.stamina
        if self.enemy.stamina + self.STAMINA_PER_ROUND * self.player.unit_class.stamina \
                <= int(self.enemy.unit_class.max_stamina):
            self.enemy.stamina += self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina

    def next_turn(self) -> str:
        """ СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
         срабатывает когда игрок пропускает ход или когда игрок наносит удар."""
        result = self._check_players_hp()
        if result:
            return result
        if self.game_is_running:
            self._stamina_regeneration()
            result = self.enemy.hit(self.player)
        return result

    def _end_game(self) -> str:
        """ КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str"""
        self._instances = {}
        result = f"{self.battle_result}\n Игра закончена!"
        # print(result)
        self.game_is_running = False
        return result

    def player_hit(self) -> str:
        """ КНОПКА УДАР ИГРОКА -> return result: str """
        result = self.player.hit(self.enemy)
        turn_result = self.next_turn()
        return f"{result}\n\n{turn_result}"

    def player_use_skill(self) -> str:
        """ КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ """
        result = self.player.use_skill(self.enemy)
        turn_result = self.next_turn()
        return f"{result}\n\n{turn_result}"