#This is just a demo. Will seriously start working on it after a couple of weeks (most likely won't). Uploaded on 3rd August, 2020. All rights not reserved.
#Whenever you see the 'Read the documentation', understand that I didn't understand it myself XD

import arcade

#Scaling of all Sprites

SPRITE_SCALING = 0.5

#SCREEN SIZE

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#VIEW PORT

VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

TILE_SIZE = 128
SCALED_TILE_SIZE = TILE_SIZE * SPRITE_SCALING
MAP_HEIGHT = 200

#The Physics

MOVEMENT_SPEED = 4
BULLET_SPEED = 20
JUMP_SPEED = 14
GRAVITY = 0.5


class MyGame(arcade.Window):
    #Create my own class which inherites from the arcade window class
    
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.MIDNIGHT_BLUE)
        self.player_list = None
        self.bullet_list = None
        self.wall_list = None
        self.player = None
        self.physics_engine = None
        self.laser_sound = arcade.load_sound("laser.ogg")
        self.view_left = 0
        self.view_bottom = 0
        self.ground_list = None
        self.environment_list = None
        

    
    def setup(self):
        #Read the arcade documentation!
        
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player = arcade.AnimatedWalkingSprite()
        
        #AnimatedWalkingSprite needs four lists 
        
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("Walk0.png"))
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("Walk0.png", mirrored = True))
        self.player.walk_right_textures = []
        self.player.walk_right_textures.append(arcade.load_texture("Walk0.png"))
        self.player.walk_right_textures.append(arcade.load_texture("Walk1.png"))
        self.player.walk_right_textures.append(arcade.load_texture("Walk2.png"))
        self.player.walk_right_textures.append(arcade.load_texture("Walk3.png"))
        
        self.player.walk_left_textures = []
        
        self.player.walk_left_textures.append(arcade.load_texture("Walk0.png", mirrored = True))
        self.player.walk_left_textures.append(arcade.load_texture("Walk1.png", mirrored = True))
        self.player.walk_left_textures.append(arcade.load_texture("Walk2.png", mirrored = True))
        self.player.walk_left_textures.append(arcade.load_texture("Walk3.png", mirrored = True))
        
        #Needs to be placed carefully, where there aren't any objects. Otherwise physics engine will raise an exception
        
        self.player.center_x = 70
        self.player.center_y = 150
        
        self.player_list.append(self.player)
        
        #Create a .tmx file using the TILED software
        
        my_map = arcade.read_tiled_map("Environment.tmx", 0.5)
        self.ground_list = arcade.generate_sprites(my_map, "ground", 0.5)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.ground_list, gravity_constant = GRAVITY)
        self.environment_list = arcade.generate_sprites(my_map, "envir", 0.5)
        
        
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("This is just a Demo",548, 358, arcade.color.WHITE, 100)
        self.environment_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.wall_list.draw()
        self.ground_list.draw()
        
    def on_update(self, delta_time):
        self.player_list.update()
        self.player_list.update_animation()
        self.physics_engine.update()
        self.bullet_list.update()
        
        #This is for the camera. Read on VIEWPORTS from the arcade documentation
        
        changed = False
        
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True
        
        if changed:
            arcade.set_viewport(self.view_left +2, SCREEN_WIDTH + self.view_left - 2, 0, 600)
    
    
    #What to do on keypresses and key releases
    
    def on_key_press(self, key, modifiers):
        
        bullet = arcade.Sprite("laserBlue01.png", 0.5 )
        bullet.center_x = self.player.center_x + 30
        bullet.center_y = self.player.center_y
        bullet.change_x = BULLET_SPEED  #Need to fix so that the bullet shoots in the direction where the player is facing, took me hours but couldn't fix lmao
        if key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        if key == arcade.key.SPACE:
            arcade.play_sound(self.laser_sound)
            self.bullet_list.append(bullet)
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED

    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.player.change_x = 0
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            print(x, y)
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Demo game by Mojo")
    window.setup()
    arcade.run()
if __name__ == "__main__":
    main()
