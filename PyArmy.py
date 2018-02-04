import hlt
import logging
import time
from operator import itemgetter

game = hlt.Game("PyArmy")
logging.info("Fast and Efficient")

while True:
    game_map = game.update_map()
    StartTime = time.time()
    Xplanet = 1.6 #lower means
    Xship = 1     #More valuable
    targeted_planets = []
    command_queue = []
    AllShips = game_map._all_ships()
    AllPlanets = game_map.all_planets()
    MyShips = game_map.get_me().all_ships()
    ControlledShips = []
    for ord1 in MyShips:
        if ord1.docking_status != ord1.DockingStatus.UNDOCKED:
            continue
        ControlledShips.append(ord1)
        
    for ship in ControlledShips:
        if time.time() - StartTime > 1.6:
            break
        ADMIN = ship.owner
        list1 = []
        for planet in AllPlanets:
            if (planet.is_full() and planet.owner == ADMIN) or (planet.owner != ADMIN and planet.owner != None):
                continue
            list1.append([planet,ship.calculate_distance_between(planet)*Xplanet])
        
        list2 = []
        for enemy_ship in AllShips:
            if enemy_ship.owner == ADMIN:
                continue
            list2.append([enemy_ship,ship.calculate_distance_between(enemy_ship)*Xship])
            
        if list1+list2 == []:
            continue
            
        list3 = sorted(list1+list2,key=itemgetter(1))
        
        list4 = []
        for ord1 in list3:
            list4.append(ord1[0])
        
        for target in list4:
            if target in AllPlanets:
                if not (target in targeted_planets):
                    if ship.can_dock(target):
                        command_queue.append(ship.dock(target))
                        targeted_planets.append(target)
                    else:
                        navigate_command = ship.navigate(
                        ship.closest_point_to(target),
                        game_map,
                        speed=7)
                        if navigate_command:
                            command_queue.append(navigate_command)
                            targeted_planets.append(target)
                    break
            else:
                navigate_command = ship.navigate(
                ship.closest_point_to(target),
                game_map,
                speed=7)
                if navigate_command:
                    command_queue.append(navigate_command)
                break
        else:
            navigate_command = ship.navigate(
            ship.closest_point_to(list4[0]),
            game_map,
            speed=7)
            targeted_planets = []
            if navigate_command:
                command_queue.append(navigate_command)
            
    game.send_command_queue(command_queue)
