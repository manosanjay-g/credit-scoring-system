<script setup>
import {ref} from 'vue'

const age = ref("")
const gender = ref("")
const income = ref("")
const marital_status = ref("")
const number_of_children = ref("")
const home_ownership = ref("")

const isShowCreditScore = ref(false)

const creditScore = ref(777)

const handleSubmit = () => {
  isShowCreditScore.value = true
}
</script>


<template>
  <div>
    <div v-if="!isShowCreditScore" class="flex flex-col items-center">
    <h1 class="font-semibold text-2xl">Add your Information</h1>
    <h1 class=" text-gray-400 text-md">This will be useful to evaluate your credit score</h1>
    <form @submit.prevent="handleSubmit" className="flex flex-col gap-3 my-4 items-center text-black">
      <input v-model="age" class=" px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md" type="text" name="Age" placeholder="Age" id="">
      <select v-model="gender" class=" px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md" name="gender" id="">
        <option value="" disabled>Select your Gender</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
      </select>
      <input v-model="income" class=" px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md" type="number" name="income" step="50000" min="100000" placeholder="Income" id=""> 
      <select v-model="marital_status" class=" px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md" name="marital_status" id="">
        <option value="" disabled>Select your Marital Status</option>
        <option value="Single">Single</option>
        <option value="Married">Married</option>
      </select>
      <input v-model="number_of_children" class=" px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md" type="number" max="5" name="number_of_children" placeholder="Number of children" id="">
      <select v-model="home_ownership" class=" px-4 bg-gray-200 focus:outline-blue-400 py-2 w-96 rounded-md" name="home_ownership" id="">
        <option value="" disabled>Select your Home Ownership</option>
        <option value="Owned">Owned</option>
        <option value="Rented">Rented</option>
      </select>
      <button class="bg-blue-500 hover:bg-blue-700 transition-all text-white w-44 px-4 py-2 rounded-md" type="submit">Check Credit Score</button>
    </form>
  </div>
  <div v-else class="flex flex-col items-center gap-4 transition-all">
    <h1 class="font-semibold text-4xl">Your credit score is</h1>
    <h1 v-if="creditScore>750" class="text-2xl text-green-600 font-semibold">{{ creditScore }}</h1>
    <h1 v-else-if="creditScore>700" class="text-2xl text-orange-400 font-semibold">{{ creditScore }}</h1>
    <h1 v-else-if="creditScore<700" class="text-2xl text-red-600 font-semibold">{{ creditScore }}</h1>
  </div>
  </div>
</template>

<style scoped></style>
