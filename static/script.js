
document.addEventListener("DOMContentLoaded", () => {
    const postIt = document.getElementById("post-it");
    if (postIt) {
        postIt.addEventListener("animationend", () => {
            postIt.style.display = "none";
        });
    }

    const gradientBackground = document.querySelector('.gradient-background');
    if (gradientBackground) { // Check if gradient-background exists
        const colors = [
            [137, 51, 235], // Purple
            [34, 19, 151],  // Dark Blue
            [255, 105, 180], // Hot Pink
            [60, 179, 113],  // Medium Sea Green
            [255, 165, 0],    // Orange
        ];
        let colorIndex = 0;
        let gradientStep = 0;
        const gradientSpeed = 0.001; // Smaller increment for smoother transition

        function animateGradient() {
            gradientStep += gradientSpeed;
            if (gradientStep >= 1) {
                gradientStep = 0;
                colorIndex = (colorIndex + 1) % colors.length;
            }

            const nextColorIndex = (colorIndex + 1) % colors.length;
            const color1 = interpolateColor(colors[colorIndex], colors[nextColorIndex], gradientStep);
            const color2 = interpolateColor(colors[nextColorIndex], colors[(nextColorIndex + 1) % colors.length], gradientStep);

            gradientBackground.style.background = `linear-gradient(90deg, rgb(${color1.join(',')}), rgb(${color2.join(',')}))`;

            requestAnimationFrame(animateGradient);
        }

        function interpolateColor(colorStart, colorEnd, factor) {
            return colorStart.map((start, index) => Math.round(start + factor * (colorEnd[index] - start)));
        }

        animateGradient();

        // Debugging: Check if animation is running
        console.log("Gradient animation started.");
    }
});