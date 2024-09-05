import { Game } from "./game.js";

document.addEventListener('DOMContentLoaded', () =>
{
    const game = new Game();
});

// TODO: Make ball change direction if it's horizontal...
// Game customization


window.addEventListener("resize", () => {
    window.location.reload();
});