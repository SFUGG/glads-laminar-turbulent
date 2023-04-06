function melt = source_moulin_shmip_steady(time, pin, dmesh)
    % melt = source_moulin_shmip_steady(time, pin, dmesh, ii_moulin, catchmap)
    % compute steady moulin inputs using SHMIP melt parameterization
    %
    % Uses 25 year winter steady-state + 25 year linear ramp-up of
    % melt intensity to ensure model stability.
    %
    % Uses average melt rate from compute_average_melt
    %
    % See also compute_average_melt

    ramp = max(0, min(time/86400/365/25 - 1, 1));

    % Load the original dmesh
    ref_meshes = load('../data/mesh/mesh.mat');
    ref_dmesh = ref_meshes.meshes{4};

    n_moulin = 68;
    moulindata = readmatrix(sprintf('./data/shmip_melt/moulins_%03d.txt', n_moulin));
    catchmap = readmatrix(sprintf('./data/shmip_melt/catchment_map_%03d.txt', n_moulin));
    ii_moulin = moulindata(:, 1) + 1;

    moulins = zeros(ref_dmesh.tri.n_nodes, 1);
    moulins(ii_moulin) = 1;

    ref_xy = dmesh.tri.nodes;

    % Read steady surface melt
    ref_steady_melt = readmatrix('SHMIP_adj_mean_melt.txt');

    ref_area = ref_dmesh.tri.area_nodes;
    ref_catch_melt = integrate_melt_by_catchment(ii_moulin, catchmap, ref_area, ref_steady_melt);

    % Now find the nearest nodes to inject melt
    xy = dmesh.tri.nodes;
    catch_melt = zeros(size(xy, 1), 1);
    for ii=1:length(ref_catch_melt)
        meltii = ref_catch_melt(ii);
        if meltii>0
            dist = sqrt((ref_xy(:, 1) - xy(:, 1)).^2 + (ref_xy(:, 2) - xy(:, 2)).^2);
            dist(catch_melt>0) = 1e10;
            [mindist, ii_min] = min(dist);
            catch_melt(ii_min) = meltii;
        end
    end


    melt = catch_melt.*ramp;
end