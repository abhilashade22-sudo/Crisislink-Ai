
(function () {
  const form = document.getElementById("sos-form");
  if (!form) return;

  const typeField = document.getElementById("sos-type");
  const detailsField = document.getElementById("sos-details");
  const manualLocation = document.getElementById("sos-location-manual");
  const locationButton = document.getElementById("sos-location-button");
  const locationStatus = document.getElementById("sos-location-status");
  const result = document.getElementById("sos-result");
  const reportField = document.getElementById("sos-report");
  const copyButton = document.getElementById("sos-copy-button");
  const copyStatus = document.getElementById("sos-copy-status");

  let coordinates = null;

  function currentTime() {
    return new Date().toLocaleString();
  }
  
  // Allow the chatbot to prefill the SOS form.
  
    window.prefillCrisisLinkSOS = function (category, details) {
  const value = String(category || "").toLowerCase();

  const categoryMap = {
    "fire": "Fire or smoke",
    "medical emergency": "Medical emergency",
    "trapped person": "Trapped person",
    "flood": "Flood",
    "accident": "Accident",
    "missing person": "Missing person",
    "crowd emergency": "Other immediate danger",
    "public safety threat": "Other immediate danger",
    "other": "Other immediate danger"
  };

  const selected = categoryMap[value];

  if (selected) {
    typeField.value = selected;
  } else if (value.includes("breath")) {
    typeField.value = "Trouble breathing";
  } else if (value.includes("unconscious")) {
    typeField.value = "Unconscious person";
  } else if (value.includes("bleed")) {
    typeField.value = "Severe bleeding";
  }

  if (details) {
    detailsField.value = String(details).slice(0, 1000);
  }

  result.hidden = true;
    };


    locationButton.addEventListener("click", function () {
    if (!navigator.geolocation) {
      locationStatus.textContent =
        "Location is not supported by this browser. Enter your address manually.";
      return;
    }

    locationStatus.textContent = "Requesting location permission...";
    locationButton.disabled = true;

    navigator.geolocation.getCurrentPosition(
      function (position) {
        coordinates = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        };

        locationStatus.textContent =
          "Location obtained. Review it before sharing.";
        locationButton.disabled = false;
      },
      function (error) {
        coordinates = null;

        const messages = {
          1: "Location permission was denied. Enter your address manually.",
          2: "Location is unavailable. Enter your address manually.",
          3: "Location request timed out. Try again or enter your address."
        };

        locationStatus.textContent =
          messages[error.code] ||
          "Could not get location. Enter your address manually.";

        locationButton.disabled = false;
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const emergencyType = typeField.value.trim();
    const details = detailsField.value.trim();
    const enteredLocation = manualLocation.value.trim();

    if (!emergencyType || !details) {
      alert("Select an emergency type and describe what happened.");
      return;
    }

    let locationText = enteredLocation || "Not provided";

    if (coordinates) {
      const coordinateText =
        coordinates.latitude.toFixed(6) +
        ", " +
        coordinates.longitude.toFixed(6);

      locationText = enteredLocation
        ? enteredLocation + " (GPS: " + coordinateText + ")"
        : "GPS coordinates: " + coordinateText;
    }

    const report = [
      "CRISISLINK AI — EMERGENCY SOS REPORT",
      "Time prepared: " + currentTime(),
      "Emergency type: " + emergencyType,
      "Location: " + locationText,
      "",
      "Situation details:",
      details,
      "",
      "IMPORTANT: This report was prepared by the user.",
      "It has NOT been automatically sent to emergency services."
    ].join("\n");

    reportField.value = report;
    result.hidden = false;
    copyStatus.textContent = "";

    result.scrollIntoView({
      behavior: "smooth",
      block: "nearest"
    });
  });

  copyButton.addEventListener("click", async function () {
    try {
      await navigator.clipboard.writeText(reportField.value);
      copyStatus.textContent =
        "Report copied. You can now paste and share it.";
    } catch (error) {
      reportField.focus();
      reportField.select();

      copyStatus.textContent =
        "Automatic copy failed. Select the report and copy it manually.";
    }
  });
})();
