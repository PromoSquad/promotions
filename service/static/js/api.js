const API_ENDPOINT = "";

function processAxiosError(error) {
  let message = "Unknown error";

  if (typeof error === "object") {
    if (
      "response" in error &&
      "data" in error.response &&
      error.response.data
    ) {
      let data = error.response.data;

      if (typeof data === "object") {
        if ("message" in data) {
          message = data.message;
        } else if ("status" in data && "error" in data) {
          message = `${data.status}: ${data.error}`;
        } else {
          message = JSON.stringify(data);
        }
      }
    } else if (error instanceof Error) {
      message = String(error.message);
    } else {
      message = JSON.stringify(error);
    }
  } else if (error) {
    message = String(error);
  }

  return message;
}

async function request(method, path, config) {
  try {
    let response = await axios.request({
      url: `${API_ENDPOINT}${path}`,
      method,
      ...config,
    });

    return response.data;
  } catch (error) {
    let message = processAxiosError(error);

    throw new Error(message);
  }
}

async function get(path, config) {
  return request("GET", path, config);
}

async function post(path, data, config) {
  return request("POST", path, { data, ...config });
}

async function put(path, data, config) {
  return request("PUT", path, { data, ...config });
}

async function del(path, config) {
  return request("DELETE", path, config);
}

async function getPromotions() {
  return get("/promotions");
}

async function getPromotionsByName(name) {
  return get(`/promotions?name=${name}`);
}

async function getPromotionsByProductId(productId) {
  return get(`/promotions?product_id=${productId}`);
}

async function getPromotionsByStatus(status) {
  return get(`/promotions?status=${status}`);
}

async function getPromotion(id) {
  return get(`/promotions/${id}`);
}

async function createPromotion(data) {
  return post("/promotions", data);
}

async function updatePromotion(id, data) {
  return put(`/promotions/${id}`, data);
}

async function deletePromotion(id) {
  return del(`/promotions/${id}`);
}
