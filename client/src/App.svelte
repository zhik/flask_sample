<script>
  import * as d3 from "d3";
  import * as turf from "@turf/turf";
  import { validate_store } from "svelte/internal";

  let date = "2023-05-13";
  let start_time = "08:30";
  let end_time = "10:30";
  let div;

  function submit(event) {
    const formData = new FormData(event.target);

    const url = `http://localhost:5000/speed?date=${formData.get(
      "date"
    )}&start=${formData.get("start_time")}&end=${formData.get("end_time")}`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        const group = d3.group(
          data,
          (d) => d.trip_id + ":" + new Date(d.timestamp).getHours()
        );
        const grouped = Array.from(group, ([key, value]) => {
          const max = d3.max(value, (d) => new Date(d.timestamp));
          const min = d3.min(value, (d) => new Date(d.timestamp));
          const seconds = (max - min) / 1000;

          let line = null;
          if (value.length > 2) {
            line = turf.lineString(
              value.map((d) => [d.longitude, d.latitude]),
              { name: "line 1" }
            );
            const length = turf.length(line, { units: "miles" });
            const mph = length / (seconds / 3600);
            return { length, mph, hour: key.split(":")[1] };
          }
          return { seconds };
        });

        const avg_per_hour = Array.from(
          d3.group(grouped, (d) => d.hour),
          ([key, value]) => {
            return { hour: key, avg: d3.mean(value, (d) => d.mph) };
          }
        )
          .filter((d) => d.hour)
          .sort((a, b) => Number(a.hour) > Number(b.hour));


        const margin = {
          top: 20,
          bottom: 0,
          left: 15,
          right: 50,
        };

        const w = div.getBoundingClientRect().width;

        const bar_width = w / 24;

        const h = 500;
        console.log(div)
        const svg = d3
          .select(div)
          .append("svg")
          .attr("width", w)
          .attr("height", h)
          .attr("viewBox", [0, 0, w, h])
          .attr("style", "max-width: 100%; height: intrinsic;");
        const bars = svg
          .append("g")
          .attr(
            "transform",
            `translate(${margin.left}, ${margin.top}) scale(1)`
          );

        const yScale = d3
          .scaleLinear()
          .domain(d3.extent(avg_per_hour, (d) => d.avg)) // unit: km
          .range([0, h - (margin.bottom + margin.top)]); // unit: pixels

        bars
          .selectAll("rect")
          .data(avg_per_hour)
          .enter()
          .append("rect")
          .attr("x", (d, i) => bar_width * Number(d.hour))
          .attr("y", (d) => yScale(d.avg))
          .attr("height", (d) => {
            console.log(h, d)
            return h - yScale(d.avg)
          })
          .attr("width", bar_width)
          .attr("fill", "#69b3a2");
      });
  }
</script>

<form action="" on:submit|preventDefault={submit}>
  <input type="date" name="date" bind:value={date} />
  <input type="time" name="start_time" bind:value={start_time} />
  <input type="time" name="end_time" bind:value={end_time} />
  <button type="submit">Query data</button>
</form>

<div bind:this={div} class="chart w-full h-64" />
