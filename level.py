import pygame
from tiles import Tile
from settings import tileSize, screenWidth, screenWidth
from player import Player
from particles import ParticlesEffect


class Level:
    def __init__(self, levelData, surface):
        # level setup
        self.displaySurface = surface
        self.levelSetup(levelData)
        self.worldShift = 0
        self.currentX = 0
        # dust
        self.dustSprite = pygame.sprite.GroupSingle()
        self.playerOnGround = False

    def getPlayerOnGrond(self):
        if self.player.sprite.onGround:
            self.playerOnGround = True
        else:
            self.playerOnGround = False

    def createLandingDust(self):
        if not self.playerOnGround and self.player.sprite.onGround and not self.dustSprite.sprites():
            if self.player.sprite.facingRight:
                offset = pygame.math.Vector2(6, 15)
            else:
                offset = pygame.math.Vector2(-6, 15)
            fallDustParticle = ParticlesEffect(
                self.player.sprite.rect.midbottom - offset, 'land')
            self.dustSprite.add(fallDustParticle)

    def creatJump(self, pos):
        if self.player.sprite.facingRight:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jumpSprite = ParticlesEffect(pos, 'jump')
        self.dustSprite.add(jumpSprite)

    def levelSetup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        
        for rowIndex, row in enumerate(layout):
            for colIndex, cell in enumerate(row):
                x = colIndex * tileSize
                y = rowIndex * tileSize
                if cell == 'X':
                    tile = Tile((x, y),     )
                    self.tiles.add(tile)
                if cell == "P":
                    playerSprite = Player(
                        (x, y), self.displaySurface, self.creatJump)
                    self.player.add(playerSprite)

    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x

        if playerX < screenWidth//2 and directionX < 0:
            self.worldShift = 3
            player.speed = 0
        elif playerX > screenWidth//2 and directionX > 0:
            self.worldShift = -3
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 3

    def xMoveColision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.onLeft = True
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.onRight = True
                    self.currentX = player.rect.right

        if player.onLeft and (player.rect.left < self.currentX or player.direction.x >= 0):
            player.onLeft = False

        if player.onRight and (player.rect.right > self.currentX or player.direction.x <= 0):
            player.onRight = False

    def yMoveColision(self):
        player = self.player.sprite
        player.applyGravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True

        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False
        if player.onCeiling and player.direction.y > 0:
            player.onCeiling = False

    def run(self):
        # dust particles
        self.dustSprite.update(self.worldShift)
        self.dustSprite.draw(self.displaySurface)
        # level tiles
        self.tiles.update(self.worldShift)
        self.tiles.draw(self.displaySurface)
        self.scrollX()  
        # player
        self.player.update()
        self.xMoveColision()
        self.getPlayerOnGrond()
        self.yMoveColision()
        self.createLandingDust()
        self.player.draw(self.displaySurface)
