<template>
  <div class="home">
    <button class="add-button" @click="$router.push('/new')">Add Quote</button>
    <hr />
    <div class="container">
      <div class="quote" v-for="quote in quotes" :key="quote.id" :quote="quote">
        <button type="button" class="delete-button" aria-label="Close" v-on:click="deleteQuote(quote.id)">
          <span aria-hidden="true">×</span>
        </button>
        <p>
          <em>"{{quote.quote}}"</em>
           {{quote.quote_by != undefined ? 'by ' + quote.quote_by : ''}}
        </p>

        <span class="added-by">added by {{quote.added_by}}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "home",
  data: () => ({
    quotes: []
  }),
  created() {
    fetch("http://localhost:8000")
      .then(res => res.json())
      .then(response => {
        this.quotes = response.quotes;
      })
      .catch(e => {
        console.error(e.message);
      });
  },
  methods: {
      deleteQuote (quoteId) {
        fetch("http://localhost:8000", {
          method: "DELETE",
          headers: {
            "Content-type": "application/json"
          },
          body: JSON.stringify({"quote_id": quoteId})
        })
          .then(res => res.json())
          .then(response => {
            if (response) {
              alert("Quote deleted successfully");
              this.$router.go();
            } else {
              alert("Oops! We could not delete your quote");
            }
          })
          .catch(e => {
            console.error(e.message);
          });
        }
    }
};
</script>


<style  scoped>
.home {
  width: 100%;
}

.add-button {
  cursor: pointer;
  border: 1px solid steelblue;
  border-radius: 5px;
  background: white;
  color: steelblue;
  height: 2em;
}

.add-button:hover {
  background: steelblue;
  color: white;
}

.delete-button {
  cursor: pointer;
  border: 0px;
  width: 32px; 
  height: 32px;
  background: transparent;
  color: grey;
  height: 2em;
  float: right;
  border-radius: 50%;
  transition: .1s;
}

.delete-button:hover {
  background-color: rgb(228, 225, 225);
  color: black;
}

.container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

.quote {
  width: 29%;
  padding: 0.5rem;
  margin: 1%;
  border-radius: 10px;
  border: 1px solid steelblue;
  color: black;
}

.quote span.by {
  text-decoration: underline;
}

.quote .added-by {
  color: rgba(0, 0, 0, 0.6);
  margin-top: 3em;
}
</style>