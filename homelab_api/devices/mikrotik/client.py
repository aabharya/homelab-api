import asyncio


class MikrotikClient:
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password

    async def run_script(self, script_name: str) -> None:
        process = await asyncio.create_subprocess_exec(
            'sshpass',
            '-p',
            self.password,
            'ssh',
            '-o',
            'StrictHostKeyChecking=no',
            f'{self.username}@{self.host}',
            f'/system script run {script_name}',
        )

        return_code = await process.wait()

        if return_code != 0:
            raise RuntimeError(f"Failed to execute MikroTik script '{script_name}'.")
