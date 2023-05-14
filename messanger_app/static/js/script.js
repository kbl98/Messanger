async function sendMessage() {
    let fd = getFormdata();
    let datum = new Date().toDateString().slice(4);
    document.getElementById("message-cont").innerHTML += `
    <div id="waiting" class="waiting"></div>`;
    try {
    
      let response = await fetch("/chat/", {
        method: "POST",
        body: fd,
      });
     let json = await response.json();
      datum = new Date(json.date).toDateString().slice(4);
      document.getElementById("waiting").remove();
      document.getElementById("message-cont").innerHTML += renderMessage(
        json.receiver.username,
        datum,
        json.text,
        json.author.username
      );
      receiverField.value = "";
      messageField.value = "";
    } catch (error) {
      alert("An Error occured");
    }
  }

  function getFormdata() {
    let fd = new FormData();
    //let token = "{{ csrf_token }}";
    fd.append("textmessage", messageField.value);
    fd.append("receiver", receiverField.value);
    fd.append("csrfmiddlewaretoken", token);
    return fd;
  }

  function renderMessage(receiver, datum, jsontext,user) {
    return ` <div class="center column row">
            <div class="row">
            <h7 class="m-side">${user}
                 to
                    ${receiver}</h7>
                    </div>
                    <div class="center column bubble margin mw200"><span class="date">${datum}</span><i>${jsontext}</i></div>
                    </div>`;
  }
