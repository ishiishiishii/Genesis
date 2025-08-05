# Laikago robot configuration
# Based on the laikago_toes.urdf file structure

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
    
    # Joint names for Laikago (4 legs * 3 joints each)
    "joint_names": [
        # Front Right leg (FR) - 1st
        "FR_hip_motor_2_chassis_joint",
        "FR_upper_leg_2_hip_motor_joint", 
        "FR_lower_leg_2_upper_leg_joint",
        # Front Left leg (FL) - 2nd
        "FL_hip_motor_2_chassis_joint",
        "FL_upper_leg_2_hip_motor_joint",
        "FL_lower_leg_2_upper_leg_joint", 
        # Rear Right leg (RR) - 3rd
        "RR_hip_motor_2_chassis_joint",
        "RR_upper_leg_2_hip_motor_joint",
        "RR_lower_leg_2_upper_leg_joint",
        # Rear Left leg (RL) - 4th
        "RL_hip_motor_2_chassis_joint", 
        "RL_upper_leg_2_hip_motor_joint",
        "RL_lower_leg_2_upper_leg_joint"
    ],
    
    # Default joint angles (standing pose)
    "default_joint_angles": {
        # Front Right leg (FR) - 1st
        "FR_hip_motor_2_chassis_joint": 0.0,
        "FR_upper_leg_2_hip_motor_joint": -0.8,
        "FR_lower_leg_2_upper_leg_joint": 1.5,
        # Front Left leg (FL) - 2nd
        "FL_hip_motor_2_chassis_joint": 0.0,
        "FL_upper_leg_2_hip_motor_joint": -0.8,
        "FL_lower_leg_2_upper_leg_joint": 1.5,
        # Rear Right leg (RR) - 3rd
        "RR_hip_motor_2_chassis_joint": 0.0,
        "RR_upper_leg_2_hip_motor_joint": -0.8,
        "RR_lower_leg_2_upper_leg_joint": 1.5,
        # Rear Left leg (RL) - 4th
        "RL_hip_motor_2_chassis_joint": 0.0,
        "RL_upper_leg_2_hip_motor_joint": -0.8,
        "RL_lower_leg_2_upper_leg_joint": 1.5
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