import { Game } from "./game.js";

document.addEventListener('DOMContentLoaded', () =>
{
    const game = new Game();
});

window.addEventListener("resize", () => {
    window.location.reload();
});