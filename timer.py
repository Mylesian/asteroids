class Timer:
    def __init__(this, time: float, start_max: bool):
        this.default_time = time
        if start_max:
            this.time = time
        else:
            this.time = 0
        
    def update(this, dt) -> bool:
        if this.time > 0:
            this.time -= dt
            return False
        
        return True

    def reset(this, time = None):
        if time == None:
            this.time = this.default_time
        else:
            this.time = time
    
creation_timer = Timer(4, True)
player_shoot_timer = Timer(0.5, False)
enemy_shoot_timer = Timer(0.5, False)