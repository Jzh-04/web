const form = document.getElementById("uploadForm");
const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const resultImage = document.getElementById("resultImage");
const labelsDiv = document.getElementById("labels");
const descriptionDiv = document.getElementById("description");
const loading = document.getElementById("loading");

imageInput.addEventListener("change", () => {
  const file = imageInput.files[0];
  if (!file) return;
  preview.src = URL.createObjectURL(file);
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = imageInput.files[0];
  if (!file) {
    alert("请先上传图片");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("detail", document.getElementById("detail").value);

  loading.classList.remove("hidden");
  labelsDiv.innerText = "处理中...";
  descriptionDiv.innerText = "处理中...";
  resultImage.src = "";

  try {
    const res = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error("后端请求失败");
    }

    const data = await res.json();

    labelsDiv.innerText = data.labels && data.labels.length > 0
      ? data.labels.join("，")
      : "未检测到标签";

    descriptionDiv.innerText = data.description || "暂无描述";

    if (data.image_url) {
      resultImage.src = data.image_url;
    }
  } catch (err) {
    console.error(err);
    labelsDiv.innerText = "请求失败";
    descriptionDiv.innerText = "请求失败，请检查后端服务和 API Key 配置。";
  } finally {
    loading.classList.add("hidden");
  }
});