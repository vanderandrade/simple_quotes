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

          <div class="autosuggest-container">
            <vue-autosuggest
                v-model="mid"
                @input="onInputChange"
                @selected="onSelected"
                @click="clickHandler"
                @focus="focusMe"
                :suggestions="filteredOptions"
                :get-suggestion-value="getSuggestionValue"
                :input-props="{id:'autosuggest__input', placeholder:'Quoter'}"
            >
              <div slot-scope="{suggestion}" style="display: flex; align-items: center;">
                <!-- <img :style="{ display: 'flex', width: '25px', height: '25px', borderRadius: '15px', marginRight: '10px'}" :src="suggestion.item.avatar" /> -->
                <div style="{ display: 'flex', color: 'navyblue'}">{{suggestion.item.name}}</div>
              </div>
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
    quoter: '',
    mid: '',
    item: {id: 9, name: 'Lion', description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.'},
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
    },
    filteredOptions() {
      return [
        { 
          data: this.suggestions[0].data.filter(option => {
            return option.name.toLowerCase().indexOf(this.mid.toLowerCase()) > -1;
          })
        }
      ];
    }
  },
  methods: {
    onSelected(item) {
      console.log('onSelect: ' + item)
      this.selected = item.item;
      this.quoter = item;
    },
    onInputChange(text) {
      console.log('onInputChange: ' + text)
    },
    getSuggestionValue(suggestion) {
      console.log('getSuggestionValue: '+ suggestion)
      return suggestion.item.name;
    },
    getLabel(item) {
      return item.name
    },

    submitQuote() {
      this.loading = false;
      this.quote['quote_by'] = this.quoter.item.name;

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
    },

    clickHandler(item) {
      console.log('clickHandler: ' + item)
    },
    focusMe(e) {
      console.log(e)
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