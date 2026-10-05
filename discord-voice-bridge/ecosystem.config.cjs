// pm2 process file:  pm2 start ecosystem.config.cjs && pm2 save && pm2 startup
module.exports = {
  apps: [
    {
      name: 'discord-voice-bridge',
      script: 'src/index.js',
      node_args: '--enable-source-maps',
      max_memory_restart: '500M',
      restart_delay: 5000,
      exp_backoff_restart_delay: 1000,
      time: true,
      env: { NODE_ENV: 'production' },
    },
  ],
};
