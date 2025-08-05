# Go2 robot configuration
# Based on the go2.urdf file structure

# Environment configuration
env_cfg = {
    "episode_length_s": 20.0,  # episode length in seconds
    "num_actions": 12,  # number of actuated joints (4 legs * 3 joints each)
    "clip_actions": 100.0,  # action clipping
    "action_scale": 0.25,  # action scaling
    "kp": 20.0,  # PD control proportional gain
    "kd": 0.5,  # PD control derivative gain
    "base_init_pos": [0.0, 0.0, 0.42],  # initial base position
    "base_init_quat": [1.0, 0.0, 0.0, 0.0],  # initial base orientation
    "termination_if_pitch_greater_than": 10,  # terminate if pitch exceeds this (degrees)
    "termination_if_roll_greater_than": 10,  # terminate if roll exceeds this (degrees)
    "resampling_time_s": 4.0,  # command resampling time
    "simulate_action_latency": True,  # simulate 1 step latency
    
    # Joint names for Go2 (4 legs * 3 joints each)
    "joint_names": [
        # Front Right leg (FR) - 1st
        "FR_hip_joint",
        "FR_thigh_joint",
        "FR_calf_joint",
        # Front Left leg (FL) - 2nd
        "FL_hip_joint",
        "FL_thigh_joint",
        "FL_calf_joint",
        # Rear Right leg (RR) - 3rd
        "RR_hip_joint",
        "RR_thigh_joint",
        "RR_calf_joint",
        # Rear Left leg (RL) - 4th
        "RL_hip_joint",
        "RL_thigh_joint",
        "RL_calf_joint"
    ],
    
    # Default joint angles (standing pose)
    "default_joint_angles": {
        # Front Left leg (FL) - 1st
        "FL_hip_joint": 0.0,
        "FL_thigh_joint": 0.8,
        "FL_calf_joint": -1.5,
        # Front Right leg (FR) - 2nd
        "FR_hip_joint": 0.0,
        "FR_thigh_joint": 0.8,
        "FR_calf_joint": -1.5,
        # Rear Left leg (RL) - 3rd
        "RL_hip_joint": 0.0,
        "RL_thigh_joint": 1.0,
        "RL_calf_joint": -1.5,
        # Rear Right leg (RR) - 4th
        "RR_hip_joint": 0.0,
        "RR_thigh_joint": 1.0,
        "RR_calf_joint": -1.5
    }
}

# Observation configuration
obs_cfg = {
    "num_obs": 45,  # 3(ang_vel) + 3(gravity) + 3(commands) + 12(dof_pos) + 12(dof_vel) + 12(actions)
    "obs_scales": {
        "lin_vel": 2.0,
        "ang_vel": 0.25,
        "dof_pos": 1.0,
        "dof_vel": 0.05
    }
}

# Reward configuration
reward_cfg = {
    "reward_scales": {
        "tracking_lin_vel": 1.0,
        "tracking_ang_vel": 0.2,
        "lin_vel_z": -1.0,
        "action_rate": -0.005,
        "similar_to_default": -0.1,
        "base_height": -50.0
    },
    "tracking_sigma": 0.25,
    "base_height_target": 0.3,
    "feet_height_target": 0.075
}

# Command configuration
command_cfg = {
    "num_commands": 3,  # linear velocity x, y and angular velocity z
    "lin_vel_x_range": [0.5, 0.5],  # forward velocity range
    "lin_vel_y_range": [0, 0],  # lateral velocity range
    "ang_vel_range": [0, 0]  # yaw velocity range
} 