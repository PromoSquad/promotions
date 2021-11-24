const app = {
  data() {
    return {
      input: {
        id: "",
        name: "",
        product_id: "",
        status: "active",
        description: "",
        type: "percentage",
        meta: "",
        begin_date: "",
        end_date: "",
      },
      metaPlaceholders: {
        percentage: '{"percentOff": 0.2}',
        coupon: '{"dollarsOff": 200.0}',
        bogo: '{"buy": 1, "get": 2}',
      },
      alert: undefined,
      searchMode: undefined,
      promotions: [],
    };
  },
  methods: {
    showError(message) {
      window.scrollTo(0, 0);
      setTimeout(() => {
        this.alert = {
          type: "danger",
          message: message,
        };
      }, 0);
    },
    showSuccess(message) {
      setTimeout(() => {
        this.alert = {
          type: "success",
          message: message,
        };
      }, 0);
    },
    clearAlert() {
      this.alert = undefined;
    },
    async onRetrieveButtonClick() {
      this.clearAlert();
      let idStr = this.input.id;
      if (idStr === "") {
        this.showError("Promotion ID cannot be empty.");
        return;
      }
      let id = Number(idStr);
      if (isNaN(id)) {
        this.showError(`Invalid Promotion ID "${idStr}".`);
        return;
      }
      try {
        let response = await getPromotion(id);
        let {
          name,
          product_id,
          active,
          description,
          type,
          meta,
          begin_date,
          end_date,
        } = response;
        if (product_id === null) {
          product_id = "";
        }
        if (description === null) {
          description = "";
        }
        if (end_date === null) {
          end_date = "";
        }
        let status = active ? "active" : "inactive";
        this.input = {
          id,
          name,
          product_id,
          status,
          description,
          type,
          meta,
          begin_date,
          end_date,
        };
        this.showSuccess(`Promotion ${id} retrieved successfully.`);
      } catch (error) {
        this.showError(error.message);
        return;
      }
    },
    async onDeleteButtonClick() {
      this.clearAlert();
      let idStr = this.input.id;
      if (idStr === "") {
        this.showError("Promotion ID cannot be empty.");
        return;
      }
      let id = Number(idStr);
      if (isNaN(id)) {
        this.showError(`Invalid Promotion ID "${idStr}".`);
        return;
      }
      try {
        await deletePromotion(id);
        this.showSuccess(`Promotion ${id} deleted successfully.`);
      } catch (error) {
        this.showError(error.message);
        return;
      }
    },
    async onActivateButtonClick() {
      this.clearAlert();
      let idStr = this.input.id;
      if (idStr === "") {
        this.showError("Promotion ID cannot be empty.");
        return;
      }
      let id = Number(idStr);
      if (isNaN(id)) {
        this.showError(`Invalid Promotion ID "${idStr}".`);
        return;
      }
      try {
        await activatePromotion(id);
        this.showSuccess(`Promotion ${id} activated successfully.`);
      } catch (error) {
        this.showError(error.message);
        return;
      }
    },
    async onDeactivateButtonClick() {
      this.clearAlert();
      let idStr = this.input.id;
      if (idStr === "") {
        this.showError("Promotion ID cannot be empty.");
        return;
      }
      let id = Number(idStr);
      if (isNaN(id)) {
        this.showError(`Invalid Promotion ID "${idStr}".`);
        return;
      }
      try {
        await deactivatePromotion(id);
        this.showSuccess(`Promotion ${id} deactivated successfully.`);
      } catch (error) {
        this.showError(error.message);
        return;
      }
    },
    onSearchRadioClick(mode) {
      if (!this.searchMode) {
        return;
      }
      this.searchMode = mode;
    },
    onBackFromSearchButtonClick() {
      if (this.input.status === "all") {
        this.input.status = "active";
      }
      this.searchMode = undefined;
    },
    async onSearchButtonClick() {
      this.clearAlert();
      if (!this.searchMode) {
        if (this.input.name) {
          this.searchMode = "name";
        } else if (this.input.product_id) {
          this.searchMode = "product_id";
        } else if (this.input.status) {
          this.searchMode = "status";
        } else {
          this.showError("Please enter a search term.");
          return;
        }
      }
      try {
        let promotions;
        switch (this.searchMode) {
          default:
          case "name":
            promotions = await getPromotionsByName(this.input.name);
            break;
          case "product_id":
            let productId = Number(this.input.product_id);
            if (isNaN(productId)) {
              this.showError(`Invalid Product ID "${this.input.product_id}".`);
              return;
            }
            promotions = await getPromotionsByProductId(this.input.product_id);
            break;
          case "status":
            if (this.input.status === "all") {
              promotions = await getPromotions();
            } else {
              promotions = await getPromotionsByStatus(this.input.status);
            }
            break;
        }
        console.log(promotions);
        this.promotions = promotions;
      } catch (error) {
        this.showError(error.message);
        return;
      }
    },
    async onCreateButtonClick() {
      this.clearAlert();
      let {
        product_id,
        name,
        type,
        description,
        meta,
        begin_date,
        end_date,
        status,
      } = this.input;
      if (product_id === "") {
        product_id = undefined;
      }
      if (description === "") {
        description = undefined;
      }
      if (begin_date === "") {
        begin_date = undefined;
      }
      if (end_date === "") {
        end_date = undefined;
      }
      try {
        let response = await createPromotion({
          product_id,
          name,
          type,
          description,
          meta,
          begin_date,
          end_date,
          active: status === "active",
        });
        let { id } = response;
        this.showSuccess(`Promotion ${id} created successfully.`);
      } catch (error) {
        this.showError(error.message);
        return;
      }
    },
    async onUpdateButtonClick() {
      this.clearAlert();
      let idStr = this.input.id;
      if (idStr === "") {
        this.showError("Promotion ID cannot be empty.");
        return;
      }
      let id = Number(idStr);
      if (isNaN(id)) {
        this.showError(`Invalid Promotion ID "${idStr}".`);
        return;
      }
      let {
        product_id,
        name,
        type,
        description,
        meta,
        begin_date,
        end_date,
        status,
      } = this.input;
      if (product_id === "") {
        product_id = undefined;
      }
      if (description === "") {
        description = undefined;
      }
      if (begin_date === "") {
        begin_date = undefined;
      }
      if (end_date === "") {
        end_date = undefined;
      }
      try {
        let response = await updatePromotion(id, {
          product_id,
          name,
          type,
          description,
          meta,
          begin_date,
          end_date,
          active: status === "active",
        });
        this.showSuccess(`Promotion ${response.id} updated successfully.`);
      } catch (error) {
        this.showError(error.message);
        return;
      }
    },
    onFillWithSampleButtonClick() {
      this.clearAlert();
      this.input = {
        id: "",
        name: "Amazing Toaster Coupon",
        product_id: "",
        status: "active",
        description: "Amazing coupon for high-end toasters",
        type: "percentage",
        meta: this.metaPlaceholders.percentage,
        begin_date: "18-Nov-2018 (08:34:58.674035)",
        end_date: "",
      };
    },
    onResetButtonClick() {
      this.clearAlert();
      this.input = {
        id: "",
        name: "",
        product_id: "",
        status: "active",
        description: "",
        type: "percentage",
        meta: "",
        begin_date: "",
        end_date: "",
      };
    },
  },
};

Vue.createApp(app).mount("#app");
