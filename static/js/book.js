var price_change = document.getElementById("price_change");
var events = document.querySelectorAll(".selectedevent");

events.forEach(function(event) {
  event.addEventListener("change", function() {
    var selectedIndex = event.selectedIndex;
    var selectedOption = event.options[selectedIndex];
    var event_id = selectedOption.getAttribute("event_id");

    fetch("http://127.0.0.1:4000/fetchprice/" + event_id, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then(function(response) {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error: " + response.status);
      }
    })
    .then(function(data) {
      price_change.textContent = "Price: " + data.data;
    })
    .catch(function(error) {
      console.error(error);
    });
  });
});
