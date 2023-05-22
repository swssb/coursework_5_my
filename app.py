from flask import Flask, render_template, request, redirect, url_for

from base import Arena
from classes import unit_classes
from equipment import EquipmentData, Equipment
from unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    """рендерим главное меню (шаблон index.html)"""
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)   ????
    arena.start_game(player=heroes["player"],enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes,result=arena.battle_result)

@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    if arena.game_is_running:
        arena.player_hit()
    render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    if arena.game_is_running:
        arena.player_use_skill()
    render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        arena.next_turn()
    render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == "GET":
        classes = unit_classes
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        header = "Выберите героя"
        result = {
            "header": header,  # для названия страниц
            "classes": classes,  # для названия классов
            "weapons": weapons,  # для названия оружия
            "armors": armors  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)
    if request.method == "POST":
        name = request.form.get("name")
        unit_class = request.form.get("unit_class")
        weapon_name = request.form.get("weapon")
        armor_name = request.form.get("armor")
        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        player.weapon = Equipment().get_weapon(weapon_name)
        player.armor = Equipment().get_armor(armor_name)
        heroes["player"] = player
        return redirect(url_for('choose_enemy'), 301)


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == "GET":
        classes = unit_classes
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        header = "Выберите героя"
        result = {
            "header": header,  # для названия страниц
            "classes": classes,  # для названия классов
            "weapons": weapons,  # для названия оружия
            "armors": armors  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)
    if request.method == "POST":
        name = request.form.get("name")
        unit_class = request.form.get("unit_class")
        weapon_name = request.form.get("weapon")
        armor_name = request.form.get("armor")
        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        enemy.weapon = Equipment().get_weapon(weapon_name)
        enemy.armor = Equipment().get_armor(armor_name)
        heroes["enemy"] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run(debug=True)
