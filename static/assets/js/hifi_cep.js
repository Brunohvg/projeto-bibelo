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
