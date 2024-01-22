
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

const set_jobs = (response) => {

  console.log(response[0])
  $("#active_running_jobs").text(JSON.stringify(response))
  const cronDiv = document.createElement("div")

  // iterate over different cron jobs
  for(let i=0; i<response.length; i++) {
    // now iterate over this single cron job
    // populate a single entry cron job table
    const currentDiv = populate_table(response[i])
    cronDiv.append(currentDiv);
    cronDiv.append(document.createElement("hr"))
  }
  // console.log(cronDiv)
  // document.body.appendChild(cronDiv)

  // console.log(document.getElementsByClassName("active_running_jobs"))
  document.getElementById("active_running_jobs").innerHTML = '';
  document.getElementById("active_running_jobs").appendChild(cronDiv)
}

function get_service_status () {
  console.log("inside function")
  $.ajax({
    async: true,
    type: 'GET',
    url: 'http://127.0.0.1:5000/running-jobs/',
    // data: { get_service_status: true },

    success: function (response) {
      //  if (response.status == 'success') {
      //    if (response.js_status)
      //      $("#js_status").attr('class', 'alert alert-success');
      //    else
      //      $("#js_status").attr('class', 'alert alert-danger');

      //    if (response.sw_status)
      //      $("#sw_status").attr('class', 'alert alert-success');
      //    else
      //      $("#sw_status").attr('class', 'alert alert-danger');

      //  }

      //  else if (response.status == 'failed') {
      //    $("#js_status").attr('class', 'alert alert-danger');
      //    $("#sw_status").attr('class', 'alert alert-danger');
      //    alert(response.message)
      //  }

      // console.log("printing response")
      // console.log(response)

      set_jobs(response)

      window.setTimeout(get_service_status, 1000)
    }
  })
  return false
}

console.log("calling the function")
get_service_status();
