// Determine if the specified layer requires authentication with an Authorization header
export const layerRequiresAuthentication = (layer) => {
  if (!layer.source || !layer.source.authenticate || !layer.login_required) {
    return false;
  }

  return true;
};

// Returns fetch parameters with Authorization header when the layer source requires authentication
// and the user is logged in
export const getFetchParameters = (layer, user) => {
  if (!layer.source || !layer.source.authenticate || !layer.login_required) {
    return {};
  }

  if (!user || !user.token) {
    return {};
  }

  return {
    headers: { Authorization: `Bearer ${user.token}` },
  };
};
