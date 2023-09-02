document.getElementById("cep").addEventListener("input", function () {
    // Remove todos os caracteres não numéricos
    const numericValue = this.value.replace(/\D/g, "");

    // Insere o hífen na posição 5 (caso haja pelo menos 5 caracteres numéricos)
    if (numericValue.length >= 5) {
        const formattedValue = numericValue.slice(0, 5) + "-" + numericValue.slice(5);
        this.value = formattedValue;
    } else {
        this.value = numericValue;
    }
});
document.querySelector("#id_telefone").addEventListener("input", function () {
    let phoneNumber = this.value.replace(/\D/g, ''); // Remove todos os caracteres não numéricos
    if (phoneNumber.length === 0) {
        this.value = ''; // Se não houver números, deixe o campo vazio
    } else if (phoneNumber.length <= 2) {
        this.value = `(${phoneNumber}`;
    } else if (phoneNumber.length <= 6) {
        this.value = `(${phoneNumber.slice(0, 2)}) ${phoneNumber.slice(2)}`;
    } else if (phoneNumber.length <= 10) {
        this.value = `(${phoneNumber.slice(0, 2)}) ${phoneNumber.slice(2, 6)}-${phoneNumber.slice(6)}`;
    } else {
        this.value = `(${phoneNumber.slice(0, 2)}) ${phoneNumber.slice(2, 7)}-${phoneNumber.slice(7, 11)}`;
    }
});
