document.addEventListener("DOMContentLoaded", () => {
    const postIt = document.getElementById("post-it");
    if (postIt) {
        postIt.addEventListener("animationend", () => {
            postIt.style.display = "none";
        });
    }

    const gradientBackground = document.querySelector('.gradient-background');
    if (gradientBackground) { // Check if gradient-background exists
        let gradientStep = 0.1;
        const gradientSpeed = 2; // Increased speed for more noticeable movement

        function animateGradient() {
            gradientStep += gradientSpeed;
            if (gradientStep > 1) {
                gradientStep = 0;
            }

            // Smoothly interpolate between purple and dark blue
            const color1 = interpolateColor([137, 51, 235], [34, 19, 151], gradientStep);
            const color2 = interpolateColor([34, 19, 151], [137, 51, 235], gradientStep);

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
