<template>
  <div class="body">
    <div class="container">
      <div v-if="loading">Loading...</div>
      <div v-else>
        <h3>New Quote</h3>

        <form @submit.prevent="submitQuote">
          <div>
            <textarea placeholder="Quote text" rows="10" v-model="quote.quote" required />
          </div>

          <div>
            <v-autocomplete type="text" placeholder="Quote by (optional)" v-model="quote.quote_by"  @update-items="updateItems"/>
          </div>

          <div>
            <input type="text" placeholder="Posted By" v-model="quote.added_by" required />
          </div>

          <div>
            <button type="submit">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    loading: false,
    quote: {},
    quoters: {}
  }),
  methods: {
    atCreation() {
        fetch("http://localhost:8000", {
          method: "GET",
          headers: {
            "Content-type": "application/json"
          },
          body: JSON.stringify({"filter": "quoters"})
        })
        .then(res => res.json())
        .then(response => {
          this.quoters = response.quotes;
        })
        .catch(e => {
          console.error(e.message);
        });
    },

    getLabel(item) {
      return item
    },
    updateItems(text) {
      this.items = quoters
    },

    submitQuote() {
      this.loading = false;

      fetch("http://localhost:8000", {
        method: "POST",
        headers: {
          "Content-type": "application/json"
        },
        body: JSON.stringify(this.quote)
      })
        .then(res => res.json())
        .then(response => {
          if (response) {
            this.$toast("Added quote!", {duration: 3000});
            this.$router.push("/");
          } else {
            this.$toast("Oops! We could not add your quote");
          }
        })
        .catch(e => {
          console.error(e.message);
        });
    }
  }
};
</script>
<style scoped >
.body {
  width: 100%;
}
h3 {
  font-weight: 300;
}

button {
  cursor: pointer;
  border: 1px solid steelblue;
  border-radius: 5px;
  background: white;
  color: steelblue;
  height: 2em;
}

button:hover {
  background: steelblue;
  color: white;
}

.container {
  width: 60%;
  margin: 15% 20% 20% 5%;
  border: 1px solid steelblue;
  padding: 2%;
}

form div {
  margin-top: 1em;
}

textarea,
input {
  width: 100%;
  font-size: 1em;
}

input:optional::placeholder {
  color: rgba(116, 116, 109, 0.578);
}
input:optional::-webkit-input-placeholder {
  color: rgba(116, 116, 109, 0.578);
}
</style>