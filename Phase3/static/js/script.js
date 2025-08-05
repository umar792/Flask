// const sendButton = document.getElementById("sendButton")



const fetchData = async (url , bodyData)=>{
    try {

        const res = await fetch(url , {
            method : "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify(bodyData)
        });

        const data = await res.json();
        if(res.ok){
            return {
                success : true,
                data
            }
        }else{
            return {
                success : false,
                message : "Error",
                data
            }
        }
        
    } catch (error) {
        return {
            success : false,
            message : error.message || "Internal Server Error"
        }
    }
}


sendButton.addEventListener("click", async ()=>{
    const inputQuestion = document.getElementById("inputQuestion").value;
    if(inputQuestion == "") return;
    console.log(inputQuestion)
    document.getElementById("inputQuestion").value = ""
    document.querySelector(".box1").style.display = "none"
    document.querySelector(".box2").style.display = "block"

    const response = await fetchData("/api", inputQuestion);
    if(response.success){
        console.log(response.data , "lll")
        const user_div = document.querySelector(".box2");
        const question_div = document.createElement("div")
        const response_div = document.createElement("div")

        question_div.innerHTML = `
           <div class="flex items-start gap-3 justify-end">  
            <div
            class="bg-[#10a37f] p-4 rounded-lg shadow-sm max-w-2xl text-white"
          >
            ${inputQuestion}
          </div>
          <div
            class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center font-semibold text-white"
          >
            U
          </div>
           </div>
            `
        user_div.appendChild(question_div)


            response_div.innerHTML = `
            <div class="flex items-start gap-3 ai_div">  
             <div
            class="w-8 h-8 bg-gray-500 rounded-full flex items-center justify-center font-semibold text-white"
          >
            A
          </div>
          <div
            class="bg-[#444654] p-4 rounded-lg shadow-sm max-w-2xl text-white bot"
          >
          ${response.data.result}
          </div>
          </div>

            
            `
        user_div.appendChild(response_div)

        
    }else{
        alert(response.message)
    }

          



    

})