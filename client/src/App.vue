<script setup>
import { ref, reactive } from "vue";
import axios from "axios";
const age = ref("");
const no_of_loans = ref("");
const no_of_delayed_payments = ref("");
const no_of_credit_inquires = ref("");
const income = ref("");
const credit_mix = ref("");
const credit_util_ratio = ref("");
const payment_behaviour = ref("");

const isShowCreditScore = ref(false);
const creditScore = ref("");
let payload = reactive({});

const handleSubmit = async () => {
  payload = {
    age: age.value,
    income: income.value,
    num_of_loans: no_of_loans.value,
    no_of_delayed_payments: no_of_delayed_payments.value,
    no_of_credit_inquires: no_of_credit_inquires.value,
    credit_mix: credit_mix.value,
    credit_util_ratio: credit_util_ratio.value,
    payment_behaviour: payment_behaviour.value,
  };
  console.log(payload);
  const res = await axios.post("http://127.0.0.1:8000/credit-score", payload);
  creditScore.value = res.data["credit_rating"];
  isShowCreditScore.value = true;

};
</script>

<template>
  <div>
    <div v-if="!isShowCreditScore" class="flex flex-col items-center">
      <h1 class="font-semibold text-2xl">Add your Information</h1>
      <h1 class="text-gray-400 text-md">
        This will be useful to evaluate your credit score
      </h1>
      <form
        @submit.prevent="handleSubmit"
        className="flex flex-col gap-3 my-4 items-center text-black"
      >
        <input
          v-model="age"
          class="px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md"
          type="text"
          name="Age"
          placeholder="Age"
          id=""
        />
        <input
          v-model="income"
          class="px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md"
          type="number"
          name="income"
          step="1000"
          min="0"
          placeholder="Income"
          id=""
        />
        <input
          v-model="no_of_loans"
          class="px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md"
          type="number"
          name="no_of_loans"
          max="50"
          min="0"
          placeholder="Number of Loans Taken"
          id=""
        />
        <input
          v-model="no_of_delayed_payments"
          class="px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md"
          type="number"
          name="no_of_delayed_payments"
          max="50"
          min="0"
          placeholder="Number of Delayed Payments"
          id=""
        />
        <input
          v-model="no_of_credit_inquires"
          class="px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md"
          type="number"
          name="no_of_credit_inquiries"
          max="50"
          min="0"
          placeholder="Number of Credit Inquiries"
          id=""
        />
        <select
          v-model="credit_mix"
          class="px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md"
          name="credit_mix"
          id=""
        >
          <option value="" disabled>Select Credit Mix</option>
          <option value="0">Bad</option>
          <option value="1">Standard</option>
          <option value="2">Good</option>
        </select>
        <input
          v-model="credit_util_ratio"
          class="px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md"
          type="number"
          min="0"
          max="100"
          name="credit_util_ratio"
          placeholder="Credit Util Ratio"
          id=""
        />
        <select
          v-model="payment_behaviour"
          class="px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md"
          name="payment_behaviour"
          id=""
        >
          <option value="" disabled>Select Payment Behaviour</option>
          <option value="10">Spent low on Small value payments</option>
          <option value="11">Spent low on Medium value payments</option>
          <option value="12">Spent low on Large value payments</option>
          <option value="20">Spent high on Small value payments</option>
          <option value="21">Spent high on Medium value payments</option>
          <option value="22">Spent high on Large value payments</option>
        </select>
        <button
          class="bg-blue-500 hover:bg-blue-700 transition-all text-white w-44 px-4 py-2 rounded-md"
          type="submit"
        >
          Check Credit Score
        </button>
      </form>
    </div>
    <div v-else class="flex flex-col items-center gap-4 transition-all">
      <h1 class="font-semibold text-4xl">Your credit score is</h1>
      <h1
        v-if="creditScore == 'High'"
        class="text-2xl text-green-600 font-semibold"
      >
        {{ creditScore }}
      </h1>
      <h1
        v-else-if="creditScore == 'Average'"
        class="text-2xl text-orange-400 font-semibold"
      >
        {{ creditScore }}
      </h1>
      <h1
        v-else-if="creditScore == 'Low'"
        class="text-2xl text-red-600 font-semibold"
      >
        {{ creditScore }}
      </h1>
    </div>
  </div>
</template>

<style scoped></style>
