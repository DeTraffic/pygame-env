Module detraffic.Vehicles
=========================

Classes
-------

`Car(x: int, y: int, width: int, height: int, accerelation: float, speed: float, direction: Direction, reward: int, color: tuple = (166, 227, 161))`
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

    `update(self, action: VehicleAction)`
    :   method to control sprite behavior
        
        Sprite.update(*args, **kwargs):
        
        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override. This method is called by
        Group.update() with whatever arguments you give it.
        
        There is no need to use this method if not using the convenience
        method by the same name in the Group class.