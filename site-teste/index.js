async function enviaPdf() {
    const input = document.getElementById("pdfFile");
    const file = input.files[0];
  
    if (!file) {
      alert("Por favor, selecione um arquivo PDF.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("resumo").textContent = "espera ai to indo pegar a resposta do chatgpt";
  
    try {
      const response = await fetch("http://localhost:8000/resumo", {
        method: "POST",
        body: formData
      });
  
      if (!response.ok) {
        const erro = await response.json();
        throw new Error(erro.detail);
      }
  
      const data = await response.json();
      document.getElementById("resumo").textContent = data.resumo;
  
    } catch (error) {
      console.error("Erro:", error);
      alert("Erro ao enviar o PDF: " + error.message);
    }
  }
  