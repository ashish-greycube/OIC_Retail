frappe.pages["outlet-map"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Outlet Map",
    single_column: true,
  });

  window.lmap = new frappe.OutletMap(page);
};
//
const marker_color_map = { Retailer: "red", "Eye Hospital": "green" };
const api_url = "https://maps.googleapis.com/maps/api/staticmap";
const zoom = "13";
const size = "600x300";
const maptype = "roadmap";
const key = "";
const sample_url = `https://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.702147,-74.015794&markers=color:green%7Clabel:G%7C40.711614,-74.012318&markers=color:red%7Clabel:C%7C40.718217,-73.998284&key=YOUR_API_KEY`;

//
frappe.OutletMap = class OutletMap {
  constructor(page) {
    this.page = page;
    this.make_form();
  }

  make_form() {
    this.form = new frappe.ui.FieldGroup({
      fields: [
        {
          label: __("Territory"),
          fieldname: "territory",
          fieldtype: "Link",
          options: "Territory",
          // change: () => this.fetch_and_render(),
        },
        {
          fieldtype: "Column Break",
        },
        {
          label: __("Outlet Type"),
          fieldname: "outlet_type",
          fieldtype: "Select",
          options: "\nEye Hospital\nOptometerist\nRetailer",
          // change: () => this.fetch_and_render(),
        },

        {
          fieldtype: "Section Break",
        },
        {
          fieldtype: "HTML",
          fieldname: "preview",
        },
      ],
      body: this.page.body,
    });

    this.form.make();
    this.load_leaflet();
    // this.load_map();
  }

  load_leaflet() {
    // debugger;
    this.form.get_field("preview").html(
      `<div class="map-wrapper border">
				<div id="leaflet-map" style="min-height: 400px; z-index: 1; max-width:100%"></div>
			</div>`
    );

    setTimeout(() => {
      L.Icon.Default.imagePath = "/assets/frappe/images/leaflet/";
      this.map = L.map("leaflet-map").setView([13, 18], 13);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(this.map);
      this.add_markers();
    }, 100);
  }

  add_markers() {
    this.get_outlets().then((arr) => {
      for (const mark of arr) {
        console.log(mark);
        L.marker(mark.lat_long).addTo(this.map).bindPopup(mark.label);
        // .openPopup();
      }

      let lat_long = arr.map((m) => {
        return m.lat_long;
      });
      let polyline = L.polyline(lat_long, {
        color: "orange",
        weight: 1,
        opacity: 0.1,
      }).addTo(this.map);
      // zoom the map to the polyline
      this.map.fitBounds(polyline.getBounds());
    });
  }

  get_outlets() {
    let filters = this.form.get_values();
    Object.assign(filters, { outlet_location: ["like", "%"] });
    return new Promise((resolve) => {
      frappe.call({
        method: "frappe.client.get_list",
        args: {
          doctype: "Retail Outlet",
          filters: filters,
          fields: ["outlet_location", "outlet_type", "outlet_name"],
          limit_page_length: 500,
        },
        callback: function (r) {
          let data = r.message.map((m) => {
            let outlet = JSON.parse(m.outlet_location);

            return {
              label: m.outlet_name,
              lat_long: outlet["features"][0]["geometry"][
                "coordinates"
              ].reverse(),
            };
          });
          resolve(data);
        },
      });
    });
  }

  get_markers(arr) {
    return arr
      .filter((m) => m.outlet_location)
      .map((m) => {
        if (!m.outlet_location) return "";
        let loc = JSON.parse(m.outlet_location);
        return {
          color: marker_color_map[m.outlet_type],
          label: m.outlet_type.slice(0, 1),
          lat_long: loc["features"][0]["geometry"]["coordinates"].join(","),
        };
      });
  }

  fetch_and_render() {
    let filters = this.form.get_values();
    this.load_map(filters);
  }

  load_map(filters = {}) {
    let me = this;
    frappe.call({
      method: "frappe.client.get_list",
      args: {
        doctype: "Retail Outlet",
        filters: filters,
        fields: ["outlet_location", "outlet_type"],
        limit_page_length: 500,
      },
      callback: function (r) {
        let markers = me
          .get_markers(r.message)
          .map((m) => `markers=color:${m.color}|label:${m.label}|${m.lat_long}`)
          .join("&amp;");

        console.log(markers);
        if (!markers.length) {
          me.form
            .get_field("preview")
            .html(
              `<h3>No Retail Outlets with location set. Please set location in Retail Outlets.</h3>`
            );
          return;
        }
        let url = encodeURI(
          `zoom=${zoom}&amp;size=${size}&amp;maptype=${maptype}&amp;${markers}&amp;key=${key}`
        );
        let alt = "OIC Retail Locations";
        let html = `<a href="${api_url}?${url}">${api_url}?${url}</a>`;
        // let html = `<img border="0" src="${api_url}?${url}"alt="${alt}">`;
        console.log(html);
        me.form.get_field("preview").html(html);
      },
    });
  }

  _load_map() {
    // let locations = [
    //   { color: "blue", label: "S", lat_long: "40.702147,-74.015794" },
    //   { color: "green", label: "G", lat_long: "40.711614,-74.012318" },
    //   { color: "red", label: "C", lat_long: "40.718217,-73.998284" },
    // ];
    // let center = "Brooklyn+Bridge,New+York,NY";
    // let markers = locations
    //   .map((m) => `markers=color:${m.color}|label:${m.label}|${m.lat_long}`)
    //   .join("&amp;");
    // let url = encodeURI(
    //   `center=${center}&amp;zoom=${zoom}&amp;size=${size}&amp;maptype=${maptype}&amp;${markers}&amp;key=${key}`
    // );
    // let alt = "OIC Retail Locations";
    // let html = `<img border="0" src="${api_url}?${url}"alt="${alt}">`;
    // this.form.get_field("preview").html(html);
  }
};
