const imgdiv = document.querySelector(
    '.profile-pic-div'
);
const img = document.querySelector('#photo');
const file = document.querySelector('#file');
const uploadbtn = document.querySelector('#uploadBtn');

imgdiv.addEventListener('mouseenter',function(){
    uploadbtn.style.display = "block";
});

imgdiv.addEventListener('mouseleave',function(){
    uploadbtn.style.display = 'none';
});

file.addEventListener('change',function(){
    const choosefile = this.files[0];
    console.log(this.files)
    if(choosefile){
        const reader = new FileReader();
        reader.addEventListener('load',function(){
            var result1 = reader.result
            console.log(result1)
            // localStorage.setItem("image",result1)
            img.setAttribute('src',reader.result);
        });
        reader.readAsDataURL(choosefile);
    }
});