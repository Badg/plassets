import jawas


@jawas.before_request
async def require_admin(self, request, *args, **kwargs):
    ''' Check the request for an 'X-User: Admin' header, raising if
    missing or invalid.
    '''


class AssetAPI(metaclass=jawas.Router, route_prefix='/assets/v1'):
    ''' Server-side asset interface.
    
    Some thoughts:
    +   Use Sqlite (in-memory) for persistence
    '''
    # The base route is responsible for all mutations.
    root = jawas.route('/<?name>')
    
    # Filter results. Note the short route prefix to prevent name collisions
    # with the assets themselves, which must have names of at least 4 chars
    sats = jawas.route('/sat')
    sats_dove = jawas.route('/sat/dove')
    sats_rapideye = jawas.route('/sat/rapideye')
    
    ants = jawas.route('/ant')
    ants_dish = jawas.route('/ant/dish')
    ants_yagi = jawas.route('/ant/yagi')
    
    @root.get
    async def root(self, request, *, name):
        ''' get on the bare root returns the entire list of assets.
        
        In a more perfect world, this would implement pagination, but
        this is too simple to justify that level of complexity here.
        
        Listing all assets will return only the asset name, type, and
        class, omitting any asset details. To get details, get the asset
        directly.
        
        Note: updating asset details is currently unsupported. The
        details themselves are optional, but cannot be changed.
        '''
        # No name was defined, so return all assets.
        if name is None:
            return self._assets
            
        # Name defined; return single asset
        else:
            return self._assets[name]
        
    @root.post
    async def root(self, request, *, name):
        ''' post on the bare root creates a new asset, or updates asset
        details.
        '''
        if name is not None:
            raise jawas.HTTP400('Client cannot assign asset name in post.')
        
        else:
            asset = Asset.from_request(request)
            self._assets[asset.name] = asset
            return asset.name
            
    @root.put
    async def root(self, request, *, name):
        ''' Update the asset at name.
        
        Note: should this be used exclusively, instead of post, forcing
        the client to always specify the name? That would make all
        operations nullipotent or idempotent.
        '''
        # Nevermind! Make all assets immutable at the moment
        raise jawas.HTTP405()
        
        if name is None:
            raise jawas.HTTP403('Client cannot overwrite all assets at once.')
            
        else:
            new_asset = Asset.from_request(request)
            old_asset = self._assets[name]
            
            inplace = (new_asset.name == old_asset.name and
                       new_asset.asset_class == old_asset.asset_class and
                       new_asset.asset_type == old_asset.asset_type)
            
            if not inplace:
                raise jawas.HTTP423('Asset names, classes, and types are ' +
                                    'immutable.')
                
            # The REST endpoint doesn't match the passed name for the asset.
            elif new_asset.name != name:
                raise jawas.HTTP409('Asset name mismatched endpoint.')
                
            else:
                self._assets[name] = new_asset
    
    
class Asset:
    ''' Client and server API base object.
    
    If more asset types start being supported, this should probably be
    refactored into a base class, with subclasses for each asset type.
    
    Thoughts: could use Asset as a metaclass to automatically generate
    type/class checks with an _Asset intermediate class.
    '''
    
    def __init__(self, name, asset_type, asset_class, **details):
        ''' Create the actual asset *locally*.
        
        Asset details are optional:
        
        antenna.dish
        {
            'diameter': float,
            'radome': bool
        }
        
        antenna.yagi
        {
            'gain': float
        }
        '''
    
    @property
    def name(self):
        ''' The asset name. Names are:
        
        +   Globally unique for all assets
        +   Immutable
        +   Alphanumeric ASCII characters, underscores, and dashes
        +   Cannot start with underscore or dash
        +   4-64 characters long
        '''
        
    @property
    def asset_type(self):
        ''' The asset type. Types are immutable and must be either:
        
        +   'satellite'
        +   'antenna'
        
        '''
        
    @property
    def asset_class(self):
        ''' The asset class. Classes are immutable and must be either:
        
        satellite:
        +   'dove'
        +   'rapideye'
        
        antenna:
        +   'dish'
        +   'yagi'
        '''
