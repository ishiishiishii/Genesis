import argparse
import os
import pickle
import shutil
from importlib import metadata

try:
    try:
        if metadata.version("rsl-rl"):
            raise ImportError
    except metadata.PackageNotFoundError:
        if metadata.version("rsl-rl-lib") != "2.2.4":
            raise ImportError
except (metadata.PackageNotFoundError, ImportError) as e:
    raise ImportError("Please uninstall 'rsl_rl' and install 'rsl-rl-lib==2.2.4'.") from e
from rsl_rl.runners import OnPolicyRunner

import genesis as gs

from laikago_env import LaikagoEnv


def get_cfgs():
    """Laikago用の設定を取得"""
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

    return env_cfg, obs_cfg, reward_cfg, command_cfg


def get_train_cfg(exp_name, max_iterations):
    train_cfg_dict = {
        "algorithm": {
            "class_name": "PPO",
            "clip_param": 0.2,
            "desired_kl": 0.01,
            "entropy_coef": 0.01,
            "gamma": 0.99,
            "lam": 0.95,
            "learning_rate": 0.001,
            "max_grad_norm": 1.0,
            "num_learning_epochs": 5,
            "num_mini_batches": 4,
            "schedule": "adaptive",
            "use_clipped_value_loss": True,
            "value_loss_coef": 1.0,
        },
        "init_member_classes": {},
        "policy": {
            "activation": "elu",
            "actor_hidden_dims": [512, 256, 128],
            "critic_hidden_dims": [512, 256, 128],
            "init_noise_std": 1.0,
            "class_name": "ActorCritic",
        },
        "runner": {
            "checkpoint": -1,
            "experiment_name": exp_name,
            "load_run": -1,
            "log_interval": 1,
            "max_iterations": max_iterations,
            "record_interval": -1,
            "resume": False,
            "resume_path": None,
            "run_name": "",
        },
        "runner_class_name": "OnPolicyRunner",
        "num_steps_per_env": 24,
        "save_interval": 10,
        "empirical_normalization": None,
        "seed": 1,
    }

    return train_cfg_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exp_name", type=str, default="laikago-walking")
    parser.add_argument("-B", "--num_envs", type=int, default=4096)
    parser.add_argument("--max_iterations", type=int, default=101)
    args = parser.parse_args()

    gs.init(logging_level="warning")

    log_dir = f"logs/{args.exp_name}"
    env_cfg, obs_cfg, reward_cfg, command_cfg = get_cfgs()
    train_cfg = get_train_cfg(args.exp_name, args.max_iterations)

    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    pickle.dump(
        [env_cfg, obs_cfg, reward_cfg, command_cfg, train_cfg],
        open(f"{log_dir}/cfgs.pkl", "wb"),
    )

    env = LaikagoEnv(
        num_envs=args.num_envs, env_cfg=env_cfg, obs_cfg=obs_cfg, reward_cfg=reward_cfg, command_cfg=command_cfg
    )

    runner = OnPolicyRunner(env, train_cfg, log_dir, device=gs.device)

    runner.learn(num_learning_iterations=args.max_iterations, init_at_random_ep_len=True)


if __name__ == "__main__":
    main()

"""
# training
python examples/locomotion/laikago_train.py
""" 