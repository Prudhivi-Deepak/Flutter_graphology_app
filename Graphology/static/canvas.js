window.addEventListener("load",()=>{
    const canvas = document.querySelector("#canvas");
    const ctx = canvas.getContext("2d");
    const color = document.querySelector("#colordone");
    const linewidthdone = document.querySelector("#linewidthdone");

    canvas.height = window.innerHeight/2;
    canvas.width = window.innerWidth/2;

    let painting = false;

    function  startposition(e){
        painting = true;
        draw(e);
    }

    function endposition(){
        painting = false;
        ctx.beginPath();
    }

    function draw(e){
        if(!painting) return ;
        // ctx.lineWidth = 2;
        ctx.lineWidth = linewidthdone.value;
        // ctx.strokeStyle='red';
        ctx.strokeStyle=color.value;
        ctx.lineCap='round';
        ctx.lineTo(e.clientX-100,e.clientY-100);
        ctx.stroke();
        // ctx.beginPath();
        // ctx.moveTo(e.clientX,e.clientY);
    }
    canvas.addEventListener('mousedown',startposition);
    canvas.addEventListener('mouseup',endposition);
    canvas.addEventListener('mousemove',draw);
    myhidden=document.getElementById("my_hidden")

    const btnsave = document.querySelector("#save");
    const image = document.querySelector("#image");

    btnsave.addEventListener('click',function(){
        const datauri = canvas.toDataURL();
        console.log(datauri);
        image.setAttribute("src",datauri);
        myhidden.value = datauri;
        // document.forms["forms1"].submit();
        // if(window.navigator.nsSaveBlob){
        //     window.navigator.nsSaveBlob(canvas.nsToBlob(),'canvas.png');
        // }
        // else{
        //     const a = document.createElement("a");
        //     document.body.appendChild(a);
        //     a.href = canvas.toDataURL("image/jpeg",0.1)
        //     a.download = "canvas.jpg";
        //     a.click();
        //     document.body.removeChild(a);
        // }
    });
});

