from gym.envs.registration import register

register(
    id='Snake-v0',
    entry_point='gym_game.envs:CustomEnv',
    max_episode_steps=2000,
)

register(
    id='Snake_hard-v0',
    entry_point='gym_game.envs:CustomEnv_hard',
    max_episode_steps=2000,
)