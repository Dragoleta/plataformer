import pygame
from support import importFolder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, createJumpDust):
        super().__init__()
        self.charAssetsImport()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft=pos)
        # dust particles
        self.importRunParticles()
        self.dustFrameIndex = 0
        self.dustAnimationSpeed = 0.15
        self.displaySurface = surface
        self.createJumpDust = createJumpDust
        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.8
        self.jumpSpeed = -15
        # player status
        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onRight = False
        self.onLeft = False

    def charAssetsImport(self):
        charPath = './assets/graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            fullPath = charPath + animation
            self.animations[animation] = importFolder(fullPath)

    def importRunParticles(self):
        self.dustRunP = importFolder(
            './assets/graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]
        # loop over frame index
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        image = self.image = animation[int(self.frameIndex)]
        if self.facingRight:
            self.image = image
        else:
            flippedImg = pygame.transform.flip(image, True, False)
            self.image = flippedImg

        # set rect
        if self.onGround and self.onRight:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.onGround and self.onLeft:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomletf)
        elif self.onGround:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.onCeiling and self.onRight:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.onCeiling and self.onLeft:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.onCeiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def runDustAnimation(self):
        if self.status == 'run' and self.onGround:
            self.dustFrameIndex += self.dustAnimationSpeed
            if self.dustFrameIndex >= len(self.dustRunP):
                self.dustFrameIndex = 0

            dustRun = self.dustRunP[int(self.dustFrameIndex)]

            if self.facingRight:
                pos = self.rect.bottomleft - pygame.math.Vector2(5, 10)
                self.displaySurface.blit(dustRun, pos)
            elif not self.facingRight:
                pos = self.rect.bottomright - pygame.math.Vector2(5, 10)
                flippedDustRun = pygame.transform.flip(dustRun, True, False)
                self.displaySurface.blit(flippedDustRun, pos)

    def jump(self):
        self.direction.y = self.jumpSpeed

    def getstatus(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def getInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facingRight = False
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facingRight = True

        elif keys[pygame.K_w]:
            pass
        elif keys[pygame.K_s]:
            pass
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.onGround:
            self.jump()
            self.createJumpDust(self.rect.midbottom)

    def update(self):
        self.getInput()
        self.getstatus()
        self.animate()
        self.runDustAnimation()
