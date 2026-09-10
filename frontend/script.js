import Vapi from "https://esm.sh/@vapi-ai/web";

const vapi = new Vapi("14f10ddf-0557-4a66-8ab0-5099c6a6fe14");

const ASSISTANT_ID = "ac890a6f-f147-4a9d-b8e0-009b31118f0e";


// =========================
// EPOCH DATA
// =========================

const epochs = {

    1450: {
        city: "Florence",
        description: "The birthplace of Renaissance art and ideas.",
        era: "The Renaissance"
    },

    1889: {
        city: "Paris",
        description: "The city of light at the dawn of the modern era.",
        era: "The Belle Époque"
    },

    1920: {
        city: "London",
        description: "A city rebuilding itself after a changing world.",
        era: "The Roaring Twenties"
    },

    2026: {
        city: "New York",
        description: "The familiar world, viewed with fresh eyes.",
        era: "The Present"
    },

    2120: {
        city: "Tokyo",
        description: "A glimpse into a technologically transformed future.",
        era: "The Near Future"
    },

    3026: {
        city: "New York",
        description: "A thousand years from today. Almost nothing is familiar.",
        era: "The Far Future"
    }

};


// =========================
// EPOCH ELEMENTS
// =========================

const epochPoints =
    document.querySelectorAll(".epoch-point");

const heroYear =
    document.getElementById("heroYear");

const heroLocation =
    document.getElementById("heroLocation");

const destinationMeta =
    document.getElementById("destinationMeta");

const destinationCity =
    document.getElementById("destinationCity");

const destinationDescription =
    document.getElementById("destinationDescription");

const travelEra =
    document.getElementById("travelEra");


// =========================
// EPOCH SELECTION
// =========================

function selectEpoch(year) {

    const epoch = epochs[year];

    if (!epoch) {
        return;
    }


    // Remove previous selection

    epochPoints.forEach(point => {

        point.classList.remove("selected");

    });


    // Select clicked epoch

    const selectedPoint =
        document.querySelector(
            `[data-year="${year}"]`
        );

    if (selectedPoint) {

        selectedPoint.classList.add("selected");

    }


    // Calculate year difference

    const currentYear = 2026;

    const difference =
        year - currentYear;

    let differenceText;


    if (difference === 0) {

        differenceText = "+0 years";

    }
    else if (difference > 0) {

        differenceText = `+${difference} years`;

    }
    else {

        differenceText = `${difference} years`;

    }


    // Update hero

    heroYear.textContent = year;

    heroLocation.textContent =
        `${epoch.city} · ${differenceText}`;


    // Update destination card

    destinationMeta.textContent =
        `◉  ${year} / ${epoch.city.toUpperCase()}`;

    destinationCity.textContent =
        epoch.city;

    destinationDescription.textContent =
        epoch.description;

    travelEra.textContent =
        epoch.era;

}


// =========================
// EPOCH CLICK EVENTS
// =========================

epochPoints.forEach(point => {

    point.addEventListener("click", () => {

        const year =
            Number(point.dataset.year);

        selectEpoch(year);

    });

});


// Default epoch

selectEpoch(2026);



// ==================================================
// NOVA / VAPI
// ==================================================


// Navbar buttons

const navNovaBtn =
    document.getElementById("navNovaBtn");

const endNovaBtn =
    document.getElementById("endNovaBtn");


// Hero buttons

const heroNovaBtn =
    document.getElementById("heroNovaBtn");

const heroEndNovaBtn =
    document.getElementById("heroEndNovaBtn");


// =========================
// INITIAL BUTTON STATE
// =========================

function showTalkButtons() {

    // Navbar

    navNovaBtn.style.display =
        "inline-flex";

    endNovaBtn.style.display =
        "none";


    // Hero

    heroNovaBtn.style.display =
        "inline-flex";

    heroEndNovaBtn.style.display =
        "none";

}


// =========================
// SHOW END CALL BUTTONS
// =========================

function showCallButtons() {

    // Navbar

    navNovaBtn.style.display =
        "none";

    endNovaBtn.style.display =
        "inline-flex";


    // Hero

    heroNovaBtn.style.display =
        "none";

    heroEndNovaBtn.style.display =
        "inline-flex";

}


// =========================
// START NOVA CALL
// =========================

function startNovaCall() {

    console.log("Starting Nova call...");

    vapi.start(ASSISTANT_ID);

}


// =========================
// END NOVA CALL
// =========================

function endNovaCall() {

    console.log("Ending Nova call...");

    vapi.stop();

}


// =========================
// VAPI CALL START EVENT
// =========================

vapi.on("call-start", () => {

    console.log("Nova call started");

    showCallButtons();

});


// =========================
// VAPI CALL END EVENT
// =========================

vapi.on("call-end", () => {

    console.log("Nova call ended");

    showTalkButtons();

});


// =========================
// BUTTON EVENTS
// =========================


// Navbar Talk

navNovaBtn.addEventListener(
    "click",
    startNovaCall
);


// Hero Talk

heroNovaBtn.addEventListener(
    "click",
    startNovaCall
);


// Navbar End Call

endNovaBtn.addEventListener(
    "click",
    endNovaCall
);


// Hero End Call

heroEndNovaBtn.addEventListener(
    "click",
    endNovaCall
);


// =========================
// INITIAL STATE
// =========================

showTalkButtons();