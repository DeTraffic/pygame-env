Module detraffic.BuildingBlocks
===============================

Classes
-------

`Intersection(x: int, y: int, lane_width: int, lane_height: int, left_to_right_lane_count: int, right_to_left_lane_count: int, top_to_bottom_lane_count: int, bottom_to_top_lane_count: int, left_to_right_car_spawn_probability: float = 0.6, right_to_left_car_spawn_probability: float = 0.6, top_to_bottom_car_spawn_probability: float = 0.6, bottom_to_top_car_spawn_probability: float = 0.6, left_to_right_special_car_spawn_probability: float = 0.05, right_to_left_special_car_spawn_probability: float = 0.05, top_to_bottom_special_car_spawn_probability: float = 0.05, bottom_to_top_special_car_spawn_probability: float = 0.05, color: tuple = (30, 30, 46))`
:   simple base class for visible game objects
    
    pygame.sprite.Sprite(*groups): return Sprite
    
    The base class for visible game objects. Derived classes will want to
    override the Sprite.update() method and assign Sprite.image and Sprite.rect
    attributes.  The initializer can accept any number of Group instances that
    the Sprite will become a member of.
    
    When subclassing the Sprite class, be sure to call the base initializer
    before adding the Sprite to Groups.

    ### Ancestors (in MRO)

    * pygame.sprite.Sprite

    ### Methods

    `draw(self, surface)`
    :   _summary_
        
        Args:
            surface (_type_): _description_

    `update(self, traffic_light_action)`
    :   method to control sprite behavior
        
        Sprite.update(*args, **kwargs):
        
        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override. This method is called by
        Group.update() with whatever arguments you give it.
        
        There is no need to use this method if not using the convenience
        method by the same name in the Group class.

`Road(x: int, y: int, going_lane_count: int, coming_lane_count: int, lane_width: int, lane_height: int, direction: Direction)`
:   simple base class for visible game objects
    
    pygame.sprite.Sprite(*groups): return Sprite
    
    The base class for visible game objects. Derived classes will want to
    override the Sprite.update() method and assign Sprite.image and Sprite.rect
    attributes.  The initializer can accept any number of Group instances that
    the Sprite will become a member of.
    
    When subclassing the Sprite class, be sure to call the base initializer
    before adding the Sprite to Groups.
    
    _summary_
    
    Args:
        x (int): _description_
        y (int): _description_
        going_lane_count (int): _description_
        coming_lane_count (int): _description_
        lane_width (int): _description_
        lane_height (int): _description_
        direction (Direction): _description_

    ### Ancestors (in MRO)

    * pygame.sprite.Sprite

    ### Methods

    `draw(self)`
    :

    `update(self)`
    :   method to control sprite behavior
        
        Sprite.update(*args, **kwargs):
        
        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override. This method is called by
        Group.update() with whatever arguments you give it.
        
        There is no need to use this method if not using the convenience
        method by the same name in the Group class.

`TrafficLight(x: int, y: int, width: int, height: int, direction: Direction)`
:   simple base class for visible game objects
    
    pygame.sprite.Sprite(*groups): return Sprite
    
    The base class for visible game objects. Derived classes will want to
    override the Sprite.update() method and assign Sprite.image and Sprite.rect
    attributes.  The initializer can accept any number of Group instances that
    the Sprite will become a member of.
    
    When subclassing the Sprite class, be sure to call the base initializer
    before adding the Sprite to Groups.
    
    _summary_
    
    Args:
        x (int): _description_
        y (int): _description_
        width (int): _description_
        height (int): _description_
        accerelation (float): _description_
        speed (float): _description_
        direction (Direction): _description_

    ### Ancestors (in MRO)

    * pygame.sprite.Sprite

    ### Methods

    `update(self, state: TrafficLightState)`
    :   method to control sprite behavior
        
        Sprite.update(*args, **kwargs):
        
        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override. This method is called by
        Group.update() with whatever arguments you give it.
        
        There is no need to use this method if not using the convenience
        method by the same name in the Group class.