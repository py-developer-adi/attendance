if (document.querySelector(".alert") != null){
    document.querySelector('.alert').style.transform = "translateY(0px)";
    document.querySelector('.alert').style.opacity = "1";
    setTimeout(() => {
        document.querySelector('.alert').style.transform = "translateY(-100px)";
        setTimeout(() => {
            document.querySelector('.alert').style.display = "none";
        }, 500);
    }, 3000);
}