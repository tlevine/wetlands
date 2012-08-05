db.runCommand({
  mapreduce : "person",
  map : function() {
    if (!this.publicNotice.processed) {emit(
      [this._id],
      {
        permitApplicationNumber: this.permitApplicationNumber,
        url: this.url,
        papertype: "public_notice"
      }
    )}
    if (!this.drawings.processed) {emit(
      [this._id],
      {
        permitApplicationNumber: this.permitApplicationNumber,
        url: this.url,
        papertype: "drawings"
      }
    )}
  },
  out: { inline: 1 },
  jsMode : true,
  verbose : true
});
