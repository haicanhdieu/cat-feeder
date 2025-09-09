import uasyncio as asyncio

class Stepper28BYJ48:
    def __init__(self, in1, in2, in3, in4, delay=2):
        self.stop_signal = False
        self.pins = [in1, in2, in3, in4]
        self.delay = delay / 1000.0  # ms to seconds
        self.sequence = [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]
        ]
        # Setup pins as output
        for pin in self.pins:
            pin.init(pin.OUT)

    async def step(self, steps, direction=1):
        seq_len = len(self.sequence)
        step_index = 0
        for _ in range(steps):
            if self.stop_signal:
                break
            step_index = (step_index + direction) % seq_len
            self._set_pins(self.sequence[step_index])
            await asyncio.sleep(self.delay)
        self._set_pins([0,0,0,0])

    def _set_pins(self, pattern):
        for pin, val in zip(self.pins, pattern):
            pin.value(val)

    async def rotate(self, degrees, direction=1):
        # 28BYJ-48: 4096 steps per revolution (gear reduction)
        steps = int(4096 * degrees / 360)
        await self.step(steps, direction)

    async def release(self):
        self._set_pins([0,0,0,0])
        
    async def turn(self, direction=1):
        """ Rotate 270 degrees in direction then rotate 90 degrees back then stop"""
        await self.rotate(120, direction)
        await self.rotate(60, -direction)
        await self.rotate(120, direction)
        await self.rotate(60, -direction)
        await self.rotate(120, direction)
        await self.rotate(60, -direction)

    async def run(self, turns, direction=1):
        """Rotate 360 degrees for n turns"""
        self.stop_signal = False
        for i in range(turns):
            await self.turn(direction)
            # Yield to other tasks between turns
            await asyncio.sleep(0)
        # Final 60 degree back to original position to pull back the food
        await self.rotate(60, -direction)
            
    async def stop(self):
        print("Stopping motor...")
        self.stop_signal = True
