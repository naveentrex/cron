const sendData = () => {
  // Get the selected values from the dropdowns
  var region = document.getElementById("region-select").value;
  var delayMode = document.getElementById("delay-mode-select").value;
  var check_function_select = document.getElementById("check-function-select").value;

  // Create an object with the form data
  var formData = {
      region: region,
      delayMode: delayMode,
      checkFunction: check_function_select
  };

  url_to_request = 'http://127.0.0.1:5000/check_data/?' + $.param(formData)
  console.log(url_to_request)

  $.ajax({
    async: true,
    type: 'GET',
    url: url_to_request,
    // contentType: "application/json",
    // data: JSON.stringify(formData),

    success: function (response) {
      populate_visualization(response['data'])
      // window.setTimeout(get_service_status, 1000)
    }
  });

}

  // console.log(region, delayMode)

const populate_table = (response) => {

  response_childrens = response["children"]
  command = response["command"].join(" ") + " -->  " + response["status"]
  // console.log(command)
  const currentDiv = document.createElement("div")
  // currentDiv.className = "cron_step"
  currentDiv.classList.add("cron_step", response["status"])
  currentDiv.innerHTML = command

  for(let i=0; i<response_childrens.length; i++) {
    currentDiv.append(populate_table(response_childrens[i]))
  }

  return currentDiv;
}

const populate_visualization = (response) => {

  // console.log(response[0])
  // const cronDiv = document.createElement("div")
  response = JSON.parse(response)
  console.log(response)
  
  // let all_regions = response.keys();
  // console.log(all_regions)
  
  for(var key in response){
    if(response.hasOwnProperty(key)){
      console.log(key, " -> ", response[key])
    }
  }


}

function get_service_status () {
  console.log("inside function")
  $.ajax({
    async: true,
    type: 'GET',
    url: 'http://127.0.0.1:5000/check_data/',
    // data: { get_service_status: true },

    success: function (response) {
      populate_visualization(response['data'])
      // window.setTimeout(get_service_status, 1000)
    }
  })
  return false
}

console.log("calling the function")
get_service_status();
// populate_visualization();
