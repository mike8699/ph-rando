<template>
  <v-app>
    <v-main>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
              >
                <v-toolbar-title>Phantom Hourglass Randomizer</v-toolbar-title>
                <v-spacer></v-spacer>
                
              </v-toolbar>
              <v-card-text>
                  <v-file-input
                  label="ROM"
                  @change="(e) => original_rom = e.path"
                  />
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="randomize">Randomize</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  import { spawnSync } from 'child_process';
  import { generateSeed } from '../randomizer/randomize';

  export default {
    props: {
      source: String,
    },

    data() {
      return {
        original_rom: '',
        output_folder: `C:/Users/micha/Desktop/ph/temp/randomized_${Date.now()}.nds`, // TODO: make this editable in the UI
      }
    },

    methods: {
      randomize() {
        const randomized_json = generateSeed();

        // TODO: make this asynchronous
        const python = spawnSync('python', ['./src/python/rom_functions.py', '--output', this.output_folder, '--rom', this.original_rom], { encoding : 'utf8', input: JSON.stringify(randomized_json) });
        console.log(python);
      },
    },
  }
</script>