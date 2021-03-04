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
            <vue-autosuggest
                :suggestions="[{data:['Frodo', 'Samwise', 'Gandalf', 'Galadriel', 'Faramir', 'Éowyn']}]"
                :input-props="{id:'autosuggest__input', placeholder:'Do you feel lucky, punk?'}"
                @input="onInputChange"
                @selected="selectHandler"
                @click="clickHandler"
            >  
              <template slot-scope="{suggestion}">
                <span class="my-suggestion-item">{{getLabel(suggestion.item)}}</span>
              </template>
            </vue-autosuggest>
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
import { VueAutosuggest } from 'vue-autosuggest';
export default {
  components: {
    VueAutosuggest
  },
  data: () => ({
    loading: false,
    quote: {},
    item: {id: 9, name: 'Lion', description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.'},
    quoters: [{data:['Frodo', 'Samwise', 'Gandalf', 'Galadriel', 'Faramir', 'Éowyn']}],
    suggestions: [
        {
          data: [
            { id: 1, name: "Frodo", race: "Hobbit", avatar: "https://upload.wikimedia.org/wikipedia/en/thumb/4/4e/Elijah_Wood_as_Frodo_Baggins.png/220px-Elijah_Wood_as_Frodo_Baggins.png" },
            { id: 2, name: "Samwise", race: "Hobbit", avatar: "https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Sean_Astin_as_Samwise_Gamgee.png/200px-Sean_Astin_as_Samwise_Gamgee.png" },
            { id: 3, name: "Gandalf", race: "Maia", avatar: "https://upload.wikimedia.org/wikipedia/en/thumb/e/e9/Gandalf600ppx.jpg/220px-Gandalf600ppx.jpg" },
            { id: 4, name: "Aragorn", race: "Human", avatar: "https://upload.wikimedia.org/wikipedia/en/thumb/3/35/Aragorn300ppx.png/150px-Aragorn300ppx.png" }
          ]
        }
      ]
  }),
  computed: {
    updateItems() {
      return this.suggestions;
    }
  },
  methods: {
    onInputChange(text) {
    },
    getSuggestionValue(suggestion) {
      return suggestion;
    },
    getLabel(item) {
      return item.name
    },

    submitQuote() {
      this.loading = false;

      fetch("http://localhost:8000", {
        method: "POST",
        headers: {"Content-type": "application/json"},
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