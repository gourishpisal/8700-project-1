from tkinter import *
import time

import const.app_config as AppConfig

from utils.delete_inactive import delete_inactive
from utils.collide import collide

window = Tk()
window.title(f"{AppConfig.GAME_NAME}")
window.geometry(f"{AppConfig.WINDOW_WIDTH}x{AppConfig.WINDOW_HEIGHT}")
window.resizable(False, False)

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

game_state = AppConfig.STORY

entered_username = ""

def on_start_click(username):
    global game_state
    game_state = AppConfig.PLAYGROUND
    global entered_username
    entered_username = username

def on_restart_click():
    global game_state
    game_state = AppConfig.STORY

def on_exit_click():
    global game_state
    game_state = "EXIT"


running = True


while running:
    if game_state == AppConfig.STORY:
        story_frame = Frame(window, height=800, width=800, bg="#000000")
        story_frame.grid(row=0, column=0, sticky="nsew")
        story_frame.grid_columnconfigure(0, weight=1)

        game_title_label = Label(
            story_frame,
            text="Haloween Hunter",
            background="#000000",
            foreground="#ffffff",
            font=('Lithos Pro Regular', 20),
            pady=20
        )
        game_title_label.grid(row=0, column=0)

        description_frame = Frame(story_frame, padx=20, pady=20, bg="#000000")
        description_frame.grid(row=1, column=0)

        line_1_text = "It's haloween and the good spirits are coming down to"
        line1 = Label(
            description_frame,
            text=line_1_text,
            background="#000000", 
            foreground="#ffffff",
            padx=20,
            pady=20,
        )
        line1.grid(row=0, column=0)

        line_2_text = "give blessings to their loved ones. But the evil spirits"
        line2 = Label(
            description_frame,
            text=line_2_text,
            background="#000000", 
            foreground="#ffffff",
            padx=20,
            pady=20,
        )
        line2.grid(row=1, column=0)

        line_3_text = "are stopping their way."
        line3 = Label(
            description_frame,
            text=line_3_text,
            background="#000000", 
            foreground="#ffffff",
            padx=20,
            pady=20,
        )
        line3.grid(row=2, column=0)

        line_4_text = "Your mission is to destroy all the evil spirits"
        line4 = Label(
            description_frame,
            text=line_4_text,
            background="#000000", 
            foreground="#ffffff",
            padx=20,
            pady=30,
        )
        line4.grid(row=3, column=0)

        line_5_text = "Best of Luck!"
        line5 = Label(
            description_frame,
            text=line_5_text,
            background="#000000", 
            foreground="#ffffff",
            padx=20,
            pady=30,
        )
        line5.grid(row=4, column=0)


        username_input = Entry(story_frame)
        username_input.insert(0, "username")
        username_input.grid(row=2, column=0, padx=20, pady=20)

        start_button = Button(story_frame, text="Start", command=lambda: on_start_click(username_input.get()))

        start_button.grid(row=3, column=0, padx=20, pady=20)
        
        story_running = True
        while story_running == True:
            if (game_state != AppConfig.STORY):
                story_running = False                
            story_frame.update()
            time.sleep(0.1)

        if (story_running == False):
            story_frame.grid_forget()
            # start_button.grid_forget()
            continue
        # story_frame.mainloop()

    elif game_state == AppConfig.PLAYGROUND:
        frame = Frame(window, width=800, height=800, background="#000000")
        frame.place(x=0, y=0)
        frame.grid_propagate(0)

        pg_canvas = Canvas(frame, width=AppConfig.PLAYGROUND_WIDTH, height=AppConfig.PLAYGROUND_HEIGHT)
        pg_canvas.place(x=100, y=100)
        # pg_canvas.grid(row=1, column=0, columnspan=2)
        bg_image = PhotoImage(file="../pic/bg.gif")
        pg_canvas.create_image(0, 0, image=bg_image, anchor="nw")

        from generate_enemy_tanks import generate_enemy_tanks
        from Tank import Tank

        enemy_tanks = generate_enemy_tanks(pg_canvas)
        enemy_bullets = []

        # Tank and bullet list for player's tanks
        player_tank = Tank(10, 10, "down", "huge", pg_canvas)
        player_bullets = []
        def shoot(event):
            player_bullets.append(player_tank.create_bullet())

        # Bind keys with respond functions
        pg_canvas.bind_all('<Up>', player_tank.set_dir_up)
        pg_canvas.bind_all('<Right>', player_tank.set_dir_right)
        pg_canvas.bind_all('<Down>', player_tank.set_dir_down)
        pg_canvas.bind_all('<Left>', player_tank.set_dir_left)
        pg_canvas.bind_all('<space>', shoot)
        
        username_label = Label(frame, text=entered_username)
        username_label.place(x=350, y = 20)
        # username_label.grid(row=0, column=0, sticky=W+E, columnspan=2)

        current_lives_text = "Lives: " + str(AppConfig.MAXIMUM_PLAYER_LIVES) + "/" + str(AppConfig.MAXIMUM_PLAYER_LIVES)
        lives_label = Label(frame, text=current_lives_text, relief=SUNKEN, anchor=W)
        # lives_label.grid(row=2, column=0, sticky=W+E)
        lives_label.place(x=10, y=750)

        score_label = Label(frame, text="Score: " + str(0), relief=SUNKEN, anchor=E)
        # score_label.grid(row=2, column=1, sticky=W+E)
        score_label.place(x=700, y=750)

        def update_status (current_lives, current_score):
            current_lives_text = "Lives: " + str(current_lives) + "/" + str(AppConfig.MAXIMUM_PLAYER_LIVES)
            global lives_label
            lives_label = Label(frame, text=current_lives_text, relief=SUNKEN, anchor=W)
            # lives_label.grid(row=2, column=0, sticky=W+E)
            lives_label.place(x=10, y=750)

            global score_label
            score_label = Label(frame, text="Score: " + str(current_score), relief=SUNKEN, anchor=E)
            # score_label.grid(row=2, column=1, sticky=W+E)
            score_label.place(x=700, y=750)


        # update_status(AppConfig.MAXIMUM_PLAYER_LIVES, 0)

        count = 0
        player_lives = AppConfig.MAXIMUM_PLAYER_LIVES
        score = 0

        pg_running = True

        while pg_running:
            # update position and images of player's tank
            player_tank.update_pos_img()

            # update position and images of enemy tanks
            for t in enemy_tanks:
                t.update_pos_img()
                if count % 20 == 0:
                    enemy_bullets.append(t.create_bullet())

            # update position and images of enemy bullets
            for b in enemy_bullets:
                b.update_state()
                b.update_pos()
                if collide(b.get_pos(), player_tank.get_pos()):
                    b.state = AppConfig.INACTIVE
                    player_tank.state = AppConfig.EXPLODE

            # update position and state of player's bullets
            for b in player_bullets:
                b.update_state()
                b.update_pos()
                for t in enemy_tanks:
                    if collide(b.get_pos(), t.get_pos()):
                        b.state = AppConfig.INACTIVE
                        t.state = AppConfig.EXPLODE

            # delete bullets that are out of window (INACTIVE)
            enemy_bullets = delete_inactive(enemy_bullets, pg_canvas)
            player_bullets = delete_inactive(player_bullets, pg_canvas)
            
            # delete tanks that finished exploding (INACTIVE)
            enemy_tanks = delete_inactive(enemy_tanks, pg_canvas)

            # calculation of lives and score
            score = (AppConfig.ENEMY_TANK_NUMBER - len(enemy_tanks))*10

            if player_tank.state == AppConfig.INACTIVE:
                player_lives -= 1
                if player_lives > 0:
                    player_tank.state = AppConfig.ACTIVE

            # canvas.itemconfig(lives_text, text='lives: '+str(player_lives))
            # canvas.itemconfig(score_text, text='score: '+str(score))
            update_status(player_lives, score)

            # check player status
            if player_tank.state == AppConfig.INACTIVE:
                # canvas.create_text(AppConfig.WINDOW_WIDTH/2, AppConfig.WINDOW_HEIGHT/2,
                #             text='YOU LOSE!nscore:'+str(score),
                #             font=('Lithos Pro Regular', 30))
                game_state = AppConfig.LEADERBOARD
                pg_running = False

            if len(enemy_tanks) == 0:
                # canvas.create_text(AppConfig.WINDOW_WIDTH / 2, AppConfig.WINDOW_HEIGHT / 2,
                #                 text='YOU WIN! score:' + str(score),
                #                 font=('Lithos Pro Regular', 30))
                game_state = AppConfig.LEADERBOARD
                pg_running = False

            count += 1
            pg_canvas.update()
            time.sleep(0.1)

        if (pg_running == False):
            score_label.grid_forget()
            username_label.grid_forget()
            score_label.grid_forget()
            lives_label.grid_forget()
            pg_canvas.grid_forget()
            frame.grid_remove()
            continue
        
        pg_canvas.mainloop()
    elif (game_state == AppConfig.LEADERBOARD):
        # story_frame = Frame(window, height=800, width=800, bg="#000000")
        # story_frame.place(x=0, y=0)
        # story_frame.place(x)
        # story_frame.grid_propagate(0)
        leaderboard_frame = Frame(window, height=800, width=800, bg="red")
        leaderboard_frame.place(x=0, y=0)
        leaderboard_frame.grid_propagate(0)
        # leaderboard_frame.pack_propagate(0)
    
        # leaderboard_canvas = Canvas(window, width=AppConfig.WINDOW_WIDTH, height=AppConfig.WINDOW_HEIGHT)
        # leaderboard_canvas.grid(row=1, column=0, columnspan=2)

        restart_button = Button(leaderboard_frame, text="Restart", command=on_restart_click, width=10)
        restart_button.place(x=200, y=750)
        
        exit_button = Button(leaderboard_frame, text="Exit", command=on_exit_click, width=10)
        exit_button.place(x=420, y=750)
        
        l_runing = True
        while l_runing == True:
            if (game_state != AppConfig.LEADERBOARD):
                l_runing = False             
            time.sleep(0.1)
            leaderboard_frame.update()


        
        if (l_runing == False):
            # print("HERE " + game_state)
            leaderboard_frame.grid_forget()
            # restart_button.grid_remove()
            # exit_button.grid_remove()
            continue
        # leaderboard_frame.mainloop()
    elif (game_state == "EXIT"):
        window.quit()
        window.destroy()

    window.update()
window.mainloop()