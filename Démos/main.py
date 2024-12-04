# Sources :
# https://www.pygame.org/news
# http://pygametutorials.wikidot.com/tutorials-basic
# https://realpython.com/pygame-a-primer/

if __name__ == "__main__":
    step: str = input("Which step do you want to execute ? ")
    match step:
        case "0":
            import pygame_step_00
            pass
        case "1":
            import pygame_step_01
            pygame_step_01.execute()
        case "2":
            import pygame_step_02
            pygame_step_02.execute()
        case "3":
            import pygame_step_03
            app: pygame_step_03.App = pygame_step_03.App()
            app.execute()
        case "4":
            import pygame_step_04
            app: pygame_step_04.App = pygame_step_04.App()
            app.execute()
        case "5":
            import pygame_step_05
            app: pygame_step_05.App = pygame_step_05.App()
            app.execute()
        case "6":
            import pygame_step_06
            app: pygame_step_06.App = pygame_step_06.App()
            app.execute()
        case "7":
            import pygame_step_07
            app: pygame_step_07.App = pygame_step_07.App()
            app.execute()
        case "8":
            import pygame_step_08
            app: pygame_step_08.App = pygame_step_08.App()
            app.execute()
        case "9":
            import pygame_step_09
            app: pygame_step_09.App = pygame_step_09.App()
            app.execute()
        case "10":
            import pygame_step_10
            app: pygame_step_10.App = pygame_step_10.App()
            app.execute()
        case "11":
            import pygame_step_11
            app: pygame_step_11.App = pygame_step_11.App()
            app.execute()
        case "12":
            import pygame_step_12
            app: pygame_step_12.App = pygame_step_12.App()
            app.execute()
        case "13":
            import pygame_step_13
            app: pygame_step_13.App = pygame_step_13.App()
            app.execute()
        case "14":
            import pygame_step_14
            app: pygame_step_14.App = pygame_step_14.App()
            app.execute()
        case "15":
            import pygame_step_15
            app: pygame_step_15.App = pygame_step_15.App()
            app.execute()
        case "16":
            import pygame_step_16
            app: pygame_step_16.App = pygame_step_16.App()
            app.execute()
        case "17":
            import pygame_step_17
            app: pygame_step_17.App = pygame_step_17.App()
            app.execute()
        case "18":
            import pygame_step_18
            app: pygame_step_18.App = pygame_step_18.App()
            app.execute()
        case "19":
            import pygame_step_19
            app: pygame_step_19.App = pygame_step_19.App()
            app.execute()
        case _:
            print("Invalid step")
