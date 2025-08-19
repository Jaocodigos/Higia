// Forms

function nextStep(sectionId, stepId) {


    const currentSection = document.getElementById(sectionId);
    const currentStep = document.getElementById(stepId);
    if (!currentSection || !currentStep) return;

    const nextSection = currentSection.nextElementSibling;
    let nextStep = currentStep.nextElementSibling;

    if (nextStep && nextStep.classList.contains("space-steps")) {
        nextStep = nextStep.nextElementSibling;
    }

    if (nextSection && nextSection.id.includes("h-form")) {


        currentSection.classList.remove("opacity-100");
        currentSection.classList.add("opacity-0");

        currentStep.classList.remove("opacity-100");
        currentStep.classList.add("opacity-40");


        setTimeout(() => {
            currentSection.classList.add("hidden");

        }, 300);

        nextSection.classList.remove("hidden");

        setTimeout(() => {

            nextSection.classList.remove("opacity-0");
            nextSection.classList.add("opacity-100");

            nextStep.classList.remove("opacity-40")
            nextStep.classList.add("opacity-100")

        }, 300);


    } else {
        console.log("Next element doesn't exist.")
    }


}

function backStep(sectionId, stepId) {

    const currentSection = document.getElementById(sectionId);
    const currentStep = document.getElementById(stepId);
    if (!currentSection || !currentStep) return;


    const previousSection = currentSection.previousElementSibling;
    let previousStep = currentStep.previousElementSibling;

    if (previousStep && previousStep.classList.contains("space-steps")) {
        previousStep = previousStep.previousElementSibling;
    }

    if (previousSection && previousSection.id.includes("h-form")) {

        currentSection.classList.add("opacity-0");
        currentSection.classList.remove("opacity-100");

        currentStep.classList.add("opacity-40");
        currentStep.classList.remove("opacity-100");


        setTimeout(() => {
            currentSection.classList.add("hidden");

        }, 300);

        previousSection.classList.remove("hidden");

        setTimeout(() => {
            previousSection.classList.add("opacity-100");
            previousSection.classList.remove("opacity-0");

            previousStep.classList.add("opacity-100");
            previousStep.classList.remove("opacity-40");

        }, 300);


    } else {
        console.log("Previous element doesn't exist.")
    }
}

