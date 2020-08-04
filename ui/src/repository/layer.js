class LayerRepository {
  static list() {
    const data = document.querySelector('#layers-data')
    if (!data) {
      return []
    }

    const layers = JSON.parse(data.innerHTML)
    if (!layers) {
      return []
    }

    return layers
  }
}

export default LayerRepository
